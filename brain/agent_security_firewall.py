from logs.logger import logger


class AgentSecurityFirewall:

    def __init__(self):

        self.agent_permissions = {}

    def register_agent(
            self,
            agent_name,
            permissions):

        self.agent_permissions[
            agent_name
        ] = permissions

        logger.info(
            f"Agent registered: {agent_name}"
        )

    def validate_access(
            self,
            agent_name,
            permission):

        permissions = (
            self.agent_permissions.get(
                agent_name,
                []
            )
        )

        return permission in permissions

    def show_agents(self):

        print(
            "\nAgent Security Firewall:\n"
        )

        if not self.agent_permissions:

            print(
                "No agents registered."
            )

            return

        for agent, permissions in (
                self.agent_permissions.items()):

            print(
                f"Agent: {agent}"
            )

            print(
                f"Permissions: "
                f"{permissions}"
            )

            print()