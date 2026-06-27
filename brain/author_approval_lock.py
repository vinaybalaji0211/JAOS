from logs.logger import logger


class AuthorApprovalLock:

    AUTHOR = "Vinay"

    PROTECTED_AREAS = [
        "source_code",
        "memory",
        "plugins",
        "secrets",
        "logs",
        "architecture",
        "configs",
        "provider_data",
        "project_roadmap"
    ]

    @staticmethod
    def check_access(
            requester,
            area,
            author_approved=False):

        if area not in AuthorApprovalLock.PROTECTED_AREAS:

            decision = "ALLOW"

        elif requester == AuthorApprovalLock.AUTHOR and author_approved:

            decision = "AUTHOR_APPROVED"

        elif requester == AuthorApprovalLock.AUTHOR:

            decision = "LOCKED"

        else:

            decision = "DENIED"

        logger.info(
            f"Author lock access check: {requester} -> {area} = {decision}"
        )

        return decision

    @staticmethod
    def show_access(
            requester,
            area,
            author_approved=False):

        decision = AuthorApprovalLock.check_access(
            requester,
            area,
            author_approved
        )

        print("\nAuthor Approval Lock:\n")

        print(f"Requester: {requester}")
        print(f"Area: {area}")
        print(f"Author Approved: {author_approved}")
        print(f"Decision: {decision}")