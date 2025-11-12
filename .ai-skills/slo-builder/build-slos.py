#!/usr/bin/env python3
"""
SLO Builder - Generates Sloth-format SLO definitions
Version: 1.0.0

Generates SLOs based on service tier and type.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml

class SLOBuilder:
    """Builds SLO definitions from templates"""

    def __init__(self, service_name: str, namespace: str, tier: str, service_type: str):
        self.service_name = service_name
        self.namespace = namespace
        self.tier = tier
        self.service_type = service_type
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load SLO templates from YAML"""
        script_dir = Path(__file__).parent
        template_file = script_dir / "slo-templates.yaml"

        try:
            with open(template_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading templates: {e}", file=sys.stderr)
            sys.exit(1)

    def _substitute_variables(self, text: str) -> str:
        """Replace template variables with actual values"""
        return (text
                .replace('{{service}}', self.service_name)
                .replace('{{namespace}}', self.namespace))

    def _generate_slo_spec(self, slo_name: str, slo_config: Dict) -> Dict:
        """Generate a single SLO spec in Sloth format"""
        return {
            'name': f"{self.service_name}-{slo_name}",
            'objective': slo_config['target'],
            'description': f"{slo_name} SLO for {self.service_name}",
            'sli': {
                'events': {
                    'errorQuery': self._substitute_variables(slo_config['sli_query'])
                }
            },
            'alerting': {
                'name': f"{self.service_name}-{slo_name}",
                'labels': {
                    'service': self.service_name,
                    'tier': self.tier,
                    'slo': slo_name
                },
                'annotations': {
                    'summary': f"High error budget burn for {slo_name}"
                },
                'pageAlert': self._generate_burn_rate_alert(slo_config, 'fast'),
                'ticketAlert': self._generate_burn_rate_alert(slo_config, 'slow')
            }
        }

    def _generate_burn_rate_alert(self, slo_config: Dict, speed: str) -> Dict:
        """Generate burn rate alert configuration"""
        if 'error_budget_burn' not in slo_config:
            return None

        burn_config = slo_config['error_budget_burn']
        window = burn_config.get(speed, '1h')

        return {
            'annotations': {
                'description': f"{speed.capitalize()} burn rate alert - {window} window"
            }
        }

    def build(self) -> Dict:
        """Build complete SLO specification"""
        # Get templates for this service type and tier
        try:
            type_templates = self.templates['templates'][self.service_type]
            tier_template = type_templates[self.tier]
        except KeyError as e:
            print(f"Error: No template found for type={self.service_type}, tier={self.tier}",
                  file=sys.stderr)
            print(f"Available types: {list(self.templates['templates'].keys())}",
                  file=sys.stderr)
            sys.exit(1)

        # Generate SLO specs
        slos = []
        for slo_name, slo_config in tier_template.items():
            slos.append(self._generate_slo_spec(slo_name, slo_config))

        # Build Sloth spec
        sloth_spec = {
            'version': 'prometheus/v1',
            'service': self.service_name,
            'labels': {
                'tier': self.tier,
                'namespace': self.namespace,
                'service_type': self.service_type
            },
            'slos': slos
        }

        return sloth_spec

    def explain(self):
        """Print human-readable explanation of generated SLOs"""
        print(f"\nSLO Configuration for {self.service_name}")
        print(f"{'=' * 60}\n")
        print(f"Service Type: {self.service_type}")
        print(f"Tier: {self.tier}")
        print(f"Namespace: {self.namespace}\n")

        try:
            type_templates = self.templates['templates'][self.service_type]
            tier_template = type_templates[self.tier]
        except KeyError:
            return

        for slo_name, slo_config in tier_template.items():
            target = slo_config['target']
            print(f"SLO: {slo_name}")
            print(f"  Target: {target}%")

            if 'threshold_ms' in slo_config:
                print(f"  Threshold: {slo_config['threshold_ms']}ms")
            elif 'threshold_minutes' in slo_config:
                print(f"  Threshold: {slo_config['threshold_minutes']} minutes")

            # Calculate error budget
            error_budget = 100 - target
            if slo_name == 'availability':
                # Convert to downtime
                monthly_minutes = 30 * 24 * 60  # ~43200 minutes
                allowed_downtime = monthly_minutes * (error_budget / 100)
                print(f"  Error Budget: {error_budget}% ({allowed_downtime:.1f} minutes/month)")
            else:
                print(f"  Error Budget: {error_budget}%")

            if 'error_budget_burn' in slo_config:
                burn = slo_config['error_budget_burn']
                print(f"  Alerts:")
                print(f"    Fast burn: Page if burning error budget in {burn['fast']}")
                print(f"    Slow burn: Ticket if burning error budget in {burn['slow']}")

            print()

def main():
    parser = argparse.ArgumentParser(
        description='Generate SLO definitions in Sloth format'
    )
    parser.add_argument('service', help='Service name')
    parser.add_argument('namespace', help='Kubernetes namespace')
    parser.add_argument(
        '--tier',
        choices=['tier-1', 'tier-2', 'tier-3'],
        required=True,
        help='Service tier'
    )
    parser.add_argument(
        '--type',
        choices=['http-api', 'grpc-service', 'batch-job', 'data-pipeline'],
        required=True,
        help='Service type'
    )
    parser.add_argument(
        '--output',
        default='slos.yaml',
        help='Output file (default: slos.yaml)'
    )
    parser.add_argument(
        '--explain',
        action='store_true',
        help='Print human-readable explanation'
    )

    args = parser.parse_args()

    builder = SLOBuilder(args.service, args.namespace, args.tier, args.type)

    if args.explain:
        builder.explain()

    # Generate SLO spec
    slo_spec = builder.build()

    # Write to file
    with open(args.output, 'w') as f:
        yaml.dump(slo_spec, f, default_flow_style=False, sort_keys=False)

    print(f"\n✓ SLO specification written to {args.output}")
    print(f"\nTo deploy:")
    print(f"  kubectl apply -f {args.output}")
    print(f"\nTo generate Prometheus rules:")
    print(f"  sloth generate -i {args.output} -o prometheus-rules.yaml")

if __name__ == '__main__':
    main()
