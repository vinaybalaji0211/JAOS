from brain.author_approval_lock import AuthorApprovalLock

AuthorApprovalLock.show_access(
    requester="Vinay",
    area="architecture",
    author_approved=False
)

AuthorApprovalLock.show_access(
    requester="Vinay",
    area="architecture",
    author_approved=True
)

AuthorApprovalLock.show_access(
    requester="Plugin",
    area="secrets",
    author_approved=False
)

AuthorApprovalLock.show_access(
    requester="Plugin",
    area="weather",
    author_approved=False
)