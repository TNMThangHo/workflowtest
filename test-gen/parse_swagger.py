import json
import argparse
import sys
import os
import requests

def load_swagger(source):
    """Load Swagger from file path or URL."""
    if source.startswith('http'):
        response = requests.get(source)
        response.raise_for_status()
        return response.json()
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"File not found: {source}")
        with open(source, 'r', encoding='utf-8') as f:
            return json.load(f)

def resolve_ref(schema, root_spec):
    """Recursively resolve $ref in schema."""
    if not isinstance(schema, dict):
        return schema
    
    if '$ref' in schema:
        ref_path = schema['$ref']
        # ref_path usually looks like "#/components/schemas/User" or "#/definitions/User"
        parts = ref_path.split('/')
        if parts[0] == '#':
            current = root_spec
            for part in parts[1:]:
                current = current.get(part, {})
            return resolve_ref(current, root_spec)
    
    # Process nested properties
    if 'properties' in schema:
        for prop, details in schema['properties'].items():
            schema['properties'][prop] = resolve_ref(details, root_spec)
            
    if 'items' in schema:
        schema['items'] = resolve_ref(schema['items'], root_spec)
        
    return schema

def parse_swagger(spec):
    """Parse spec and return simplified structure."""
    simplified_specs = []
    
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                continue
                
            summary = details.get('summary', 'No summary')
            description = details.get('description', '')
            
            # 1. Parameters
            params = []
            raw_params = details.get('parameters', [])
            for p in raw_params:
                p_resolved = resolve_ref(p, spec)
                params.append({
                    "name": p_resolved.get('name'),
                    "in": p_resolved.get('in'),
                    "required": p_resolved.get('required', False),
                    "type": p_resolved.get('schema', {}).get('type', 'unknown'),
                    "description": p_resolved.get('description', '')
                })
                
            # 2. Request Body
            body_schema = {}
            if 'requestBody' in details:
                content = details['requestBody'].get('content', {})
                if 'application/json' in content:
                    raw_schema = content['application/json'].get('schema', {})
                    body_schema = resolve_ref(raw_schema, spec)
            
            # 3. Responses
            responses = []
            for status, resp in details.get('responses', {}).items():
                resp_desc = resp.get('description', '')
                responses.append({"status": status, "description": resp_desc})
                
            technical_spec = {
                "endpoint": f"{method.upper()} {path}",
                "summary": summary,
                "description": description,
                "parameters": params,
                "request_body": body_schema,
                "responses": responses
            }
            
            simplified_specs.append(technical_spec)
            
    return simplified_specs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Swagger/OpenAPI file to simplified JSON")
    parser.add_argument("--input", required=True, help="Path or URL to Swagger JSON")
    parser.add_argument("--output", help="Output JSON file path", default="output/technical_specs.json")
    
    args = parser.parse_args()
    
    try:
        spec = load_swagger(args.input)
        simplified = parse_swagger(spec)
        
        output_data = {
            "source": args.input,
            "total_endpoints": len(simplified),
            "specs": simplified
        }
        
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
            
        print(f"Successfully parsed {len(simplified)} endpoints. Saved to {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
