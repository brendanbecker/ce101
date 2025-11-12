#!/usr/bin/env python3
"""
Production Readiness Review Automated Checker
Version: 2.1.0

Validates Kubernetes deployments against PRR requirements.
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

class Colors:
    """ANSI color codes for output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class CheckResult:
    """Result of a single check"""
    def __init__(self, requirement_id: str, name: str, passed: bool,
                 severity: str, message: str, details: Optional[str] = None):
        self.requirement_id = requirement_id
        self.name = name
        self.passed = passed
        self.severity = severity
        self.message = message
        self.details = details

class PRRChecker:
    """Production Readiness Review automated checker"""

    def __init__(self, service_name: str, namespace: str, tier: str = "tier-1"):
        self.service_name = service_name
        self.namespace = namespace
        self.tier = tier
        self.results: List[CheckResult] = []
        self.requirements = self._load_requirements()

    def _load_requirements(self) -> Dict:
        """Load PRR requirements from YAML file"""
        script_dir = Path(__file__).parent
        req_file = script_dir / "prr-requirements.yaml"

        try:
            with open(req_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"{Colors.RED}Error loading requirements: {e}{Colors.RESET}")
            sys.exit(1)

    def _run_kubectl(self, args: List[str]) -> Optional[Dict]:
        """Run kubectl command and return JSON output"""
        try:
            cmd = ['kubectl', '-n', self.namespace] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
            return None
        except subprocess.CalledProcessError:
            return None
        except json.JSONDecodeError as e:
            print(f"{Colors.YELLOW}Warning: Could not parse kubectl output: {e}{Colors.RESET}")
            return None

    def _get_deployment(self) -> Optional[Dict]:
        """Get deployment manifest"""
        return self._run_kubectl([
            'get', 'deployment', self.service_name,
            '-o', 'json'
        ])

    def _get_service(self) -> Optional[Dict]:
        """Get service manifest"""
        return self._run_kubectl([
            'get', 'service', self.service_name,
            '-o', 'json'
        ])

    def _get_servicemonitor(self) -> Optional[Dict]:
        """Get ServiceMonitor manifest"""
        return self._run_kubectl([
            'get', 'servicemonitor', self.service_name,
            '-o', 'json'
        ])

    def _get_prometheusrule(self) -> Optional[Dict]:
        """Get PrometheusRule manifest"""
        return self._run_kubectl([
            'get', 'prometheusrule', f"{self.service_name}-alerts",
            '-o', 'json'
        ])

    def _get_networkpolicy(self) -> Optional[Dict]:
        """Get NetworkPolicy manifest"""
        return self._run_kubectl([
            'get', 'networkpolicy', self.service_name,
            '-o', 'json'
        ])

    def check_deployment_has_metrics_port(self, deployment: Dict) -> CheckResult:
        """MON-001: Check if deployment has metrics port"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'MON-001')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            for container in containers:
                if 'ports' in container:
                    for port in container['ports']:
                        if port.get('name') == 'metrics':
                            return CheckResult(
                                req['id'], req['name'], True, req['severity'],
                                f"Metrics port found: {port.get('containerPort')}"
                            )

            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "No port named 'metrics' found in deployment",
                "Add a container port named 'metrics' (typically 8080 or 9090)"
            )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing deployment: {e}"
            )

    def check_servicemonitor_exists(self) -> CheckResult:
        """MON-002: Check if ServiceMonitor exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'MON-002')

        sm = self._get_servicemonitor()
        if sm:
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                "ServiceMonitor configured"
            )
        else:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "ServiceMonitor not found",
                f"Create a ServiceMonitor resource for {self.service_name}"
            )

    def check_prometheusrule_exists(self) -> CheckResult:
        """MON-003: Check if PrometheusRule exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'MON-003')

        pr = self._get_prometheusrule()
        if pr:
            try:
                rules = pr['spec']['groups'][0]['rules']
                num_alerts = len([r for r in rules if r.get('alert')])
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    f"PrometheusRule found with {num_alerts} alert(s)"
                )
            except (KeyError, IndexError):
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    "PrometheusRule exists but has no alerts defined"
                )
        else:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "PrometheusRule not found",
                f"Create a PrometheusRule resource named {self.service_name}-alerts"
            )

    def check_file_exists(self, filepath: str, req_id: str) -> CheckResult:
        """DOC-001, DOC-002: Check if documentation file exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == req_id)

        # Check in current directory
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            if file_size < 100:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    f"{filepath} exists but appears too short ({file_size} bytes)",
                    "Ensure documentation is comprehensive"
                )
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                f"{filepath} exists ({file_size} bytes)"
            )
        else:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"{filepath} not found",
                f"Create {filepath} with comprehensive documentation"
            )

    def check_security_context(self, deployment: Dict) -> CheckResult:
        """SEC-001: Check if security context is configured"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'SEC-001')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            spec = deployment['spec']['template']['spec']
            security_context = spec.get('securityContext', {})

            issues = []

            if not security_context.get('runAsNonRoot'):
                issues.append("runAsNonRoot not set to true")

            # Check container security contexts
            containers = spec.get('containers', [])
            for container in containers:
                container_sc = container.get('securityContext', {})
                if not container_sc.get('readOnlyRootFilesystem'):
                    issues.append(f"readOnlyRootFilesystem not set for container {container['name']}")

            if issues:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    "Security context issues found",
                    "; ".join(issues)
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    "Security context properly configured"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing deployment security context: {e}"
            )

    def check_no_plaintext_secrets(self, deployment: Dict) -> CheckResult:
        """SEC-002: Check for plaintext secrets in env vars"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'SEC-002')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            suspicious_vars = []

            for container in containers:
                env_vars = container.get('env', [])
                for env_var in env_vars:
                    # Check if env var has direct value (not from secret/configmap)
                    if 'value' in env_var and not ('valueFrom' in env_var):
                        var_name = env_var['name'].lower()
                        # Check for common secret patterns
                        if any(pattern in var_name for pattern in ['password', 'secret', 'token', 'key', 'api']):
                            suspicious_vars.append(env_var['name'])

            if suspicious_vars:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    f"Potential plaintext secrets found: {', '.join(suspicious_vars)}",
                    "Use Kubernetes Secrets or valueFrom with secretKeyRef"
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    "No plaintext secrets detected"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing environment variables: {e}"
            )

    def check_networkpolicy_exists(self) -> CheckResult:
        """SEC-003: Check if NetworkPolicy exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'SEC-003')

        # Check if tier requires this
        if req['tiers'][self.tier] == 'optional':
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                f"Optional for {self.tier} - skipped"
            )

        np = self._get_networkpolicy()
        if np:
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                "NetworkPolicy configured"
            )
        else:
            severity = 'warning' if req['tiers'][self.tier] == 'recommended' else req['severity']
            return CheckResult(
                req['id'], req['name'], False, severity,
                "NetworkPolicy not found",
                f"Create a NetworkPolicy for {self.service_name}"
            )

    def check_replica_count(self, deployment: Dict) -> CheckResult:
        """REL-001: Check replica count"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'REL-001')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            replicas = deployment['spec']['replicas']

            min_replicas = 2 if self.tier == 'tier-1' else 1

            if replicas >= min_replicas:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    f"Replica count: {replicas} (minimum: {min_replicas})"
                )
            else:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    f"Insufficient replicas: {replicas} (minimum: {min_replicas})",
                    f"Increase replicas to at least {min_replicas} for {self.tier}"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing replica count: {e}"
            )

    def check_resources_defined(self, deployment: Dict) -> CheckResult:
        """REL-002: Check if resource requests/limits are defined"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'REL-002')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            issues = []

            for container in containers:
                resources = container.get('resources', {})
                requests = resources.get('requests', {})
                limits = resources.get('limits', {})

                if not requests.get('memory'):
                    issues.append(f"{container['name']}: missing memory request")
                if not requests.get('cpu'):
                    issues.append(f"{container['name']}: missing CPU request")
                if not limits.get('memory'):
                    issues.append(f"{container['name']}: missing memory limit")
                if not limits.get('cpu'):
                    issues.append(f"{container['name']}: missing CPU limit")

            if issues:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    "Resource issues found",
                    "; ".join(issues)
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    "Resource requests and limits configured"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing resources: {e}"
            )

    def check_probe(self, deployment: Dict, probe_type: str, req_id: str) -> CheckResult:
        """REL-003, REL-004: Check if liveness/readiness probe is configured"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == req_id)

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            probe_name = f"{probe_type}Probe"
            missing_containers = []

            for container in containers:
                if probe_name not in container:
                    missing_containers.append(container['name'])

            if missing_containers:
                severity = req['severity'] if req['tiers'][self.tier] == 'required' else 'warning'
                return CheckResult(
                    req['id'], req['name'], False, severity,
                    f"{probe_type.capitalize()} probe missing for: {', '.join(missing_containers)}",
                    f"Add {probe_name} to container spec"
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    f"{probe_type.capitalize()} probe configured for all containers"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing {probe_type} probe: {e}"
            )

    def run_checks(self) -> List[CheckResult]:
        """Run all automated checks"""
        print(f"\n{Colors.BOLD}Production Readiness Review{Colors.RESET}")
        print(f"Service: {self.service_name}")
        print(f"Namespace: {self.namespace}")
        print(f"Tier: {self.tier}\n")

        # Fetch resources
        print("Fetching Kubernetes resources...")
        deployment = self._get_deployment()

        # Run all automated checks
        self.results.append(self.check_deployment_has_metrics_port(deployment))
        self.results.append(self.check_servicemonitor_exists())
        self.results.append(self.check_prometheusrule_exists())
        self.results.append(self.check_file_exists('README.md', 'DOC-001'))
        self.results.append(self.check_file_exists('RUNBOOK.md', 'DOC-002'))
        self.results.append(self.check_security_context(deployment))
        self.results.append(self.check_no_plaintext_secrets(deployment))
        self.results.append(self.check_networkpolicy_exists())
        self.results.append(self.check_replica_count(deployment))
        self.results.append(self.check_resources_defined(deployment))
        self.results.append(self.check_probe(deployment, 'liveness', 'REL-003'))
        self.results.append(self.check_probe(deployment, 'readiness', 'REL-004'))

        return self.results

    def print_results(self):
        """Print check results in a formatted way"""
        passed = [r for r in self.results if r.passed]
        failed = [r for r in self.results if not r.passed]

        print(f"\n{Colors.BOLD}Automated Check Results:{Colors.RESET}\n")

        # Print failures first
        if failed:
            print(f"{Colors.RED}{Colors.BOLD}FAILED CHECKS:{Colors.RESET}")
            for result in failed:
                color = Colors.RED if result.severity == 'blocker' else Colors.YELLOW
                print(f"\n{color}✗ [{result.requirement_id}] {result.name}{Colors.RESET}")
                print(f"  {result.message}")
                if result.details:
                    print(f"  → {result.details}")

        # Print successes
        if passed:
            print(f"\n{Colors.GREEN}{Colors.BOLD}PASSED CHECKS:{Colors.RESET}")
            for result in passed:
                print(f"{Colors.GREEN}✓ [{result.requirement_id}] {result.name}{Colors.RESET}")
                print(f"  {result.message}")

        # Summary
        print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
        print(f"Total checks: {len(self.results)}")
        print(f"{Colors.GREEN}Passed: {len(passed)}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {len(failed)}{Colors.RESET}")

        blockers = [r for r in failed if r.severity == 'blocker']
        if blockers:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠ {len(blockers)} blocker(s) must be resolved before production launch{Colors.RESET}")
            return 1
        else:
            print(f"\n{Colors.GREEN}All blockers passed! Review manual checks before launch.{Colors.RESET}")
            return 0

def main():
    parser = argparse.ArgumentParser(
        description='Production Readiness Review automated checker'
    )
    parser.add_argument('service', help='Service name')
    parser.add_argument('namespace', help='Kubernetes namespace')
    parser.add_argument(
        '--tier',
        choices=['tier-1', 'tier-2', 'tier-3'],
        default='tier-1',
        help='Service tier (default: tier-1)'
    )
    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    checker = PRRChecker(args.service, args.namespace, args.tier)
    results = checker.run_checks()

    if args.output == 'json':
        output = {
            'service': args.service,
            'namespace': args.namespace,
            'tier': args.tier,
            'results': [
                {
                    'id': r.requirement_id,
                    'name': r.name,
                    'passed': r.passed,
                    'severity': r.severity,
                    'message': r.message,
                    'details': r.details
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    else:
        sys.exit(checker.print_results())

if __name__ == '__main__':
    main()
