#!/usr/bin/env python3
"""Read-only MCP stdio server. JSON-RPC messages are newline delimited."""
import argparse
import json
from pathlib import Path
import sys

ARTIFACTS = ('brief.md', 'knowledge-map.md', 'learning-path.md', 'storyboard.md', 'quality-gates.md', 'run-state.md')
TOOLS = [
    {'name': 'artifact_status', 'description': 'Check artifact presence; does not validate pedagogical quality or pass gates.', 'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'name': 'read_artifact', 'description': 'Read one allowlisted LX document (maximum 128 KiB).', 'inputSchema': {'type': 'object', 'properties': {'name': {'type': 'string', 'enum': list(ARTIFACTS)}}, 'required': ['name'], 'additionalProperties': False}},
]


def artifact_path(root, name):
    if name not in ARTIFACTS:
        raise ValueError('Document is not allowlisted')
    path = (root / 'docs' / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Document escapes project root')
    return path


def call_tool(root, name, arguments):
    if name == 'artifact_status' and arguments == {}:
        status = {}
        for item in ARTIFACTS:
            try:
                p = artifact_path(root, item)
                status[item] = 'present' if p.is_file() and p.stat().st_size else 'missing-or-empty'
            except ValueError:
                status[item] = 'blocked-path'
        return json.dumps({'artifacts': status, 'semantic_gates': 'not-evaluated'}, ensure_ascii=False)
    if name == 'read_artifact' and set(arguments) == {'name'}:
        p = artifact_path(root, arguments['name'])
        with p.open('rb') as stream:
            data = stream.read(131073)
        if len(data) > 131072:
            raise ValueError('Document exceeds 128 KiB; read it with project tools')
        return data.decode('utf-8')
    raise ValueError('Unknown tool or invalid arguments')


def handle(root, request):
    if 'id' not in request:
        return None
    reply = {'jsonrpc': '2.0', 'id': request['id']}
    method = request.get('method')
    params = request.get('params', {})
    if method == 'initialize':
        version = params.get('protocolVersion', '2024-11-05')
        if version not in ('2024-11-05', '2025-03-26', '2025-06-18', '2025-11-25'):
            version = '2024-11-05'
        reply['result'] = {'protocolVersion': version, 'capabilities': {'tools': {}}, 'serverInfo': {'name': 'lx-artifacts', 'version': '1.0.0'}}
    elif method == 'ping':
        reply['result'] = {}
    elif method == 'tools/list':
        reply['result'] = {'tools': TOOLS}
    elif method == 'tools/call':
        try:
            result = call_tool(root, params.get('name'), params.get('arguments', {}))
            reply['result'] = {'content': [{'type': 'text', 'text': result}]}
        except (OSError, ValueError, TypeError) as error:
            reply['result'] = {'isError': True, 'content': [{'type': 'text', 'text': str(error)}]}
    else:
        reply['error'] = {'code': -32601, 'message': 'Method not found'}
    return reply


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    root = parser.parse_args().root.resolve()
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise ValueError('Expected request object')
            response = handle(root, request)
        except (ValueError, TypeError, AttributeError):
            response = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'Invalid JSON-RPC message'}}
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
