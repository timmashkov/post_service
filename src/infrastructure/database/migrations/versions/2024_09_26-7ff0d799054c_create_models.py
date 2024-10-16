"""create models

Revision ID: 7ff0d799054c
Revises: 
Create Date: 2024-09-26 17:30:33.914699

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7ff0d799054c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "profiles",
        sa.Column("user_uuid", sa.String(), nullable=False, comment="УУИД юзера"),
        sa.Column("first_name", sa.String(length=20), nullable=False),
        sa.Column("last_name", sa.String(length=30), nullable=False),
        sa.Column("occupation", sa.String(length=30), nullable=True),
        sa.Column("status", sa.Text(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("user_uuid"),
    )
    op.create_table(
        "friends",
        sa.Column("profile_id", sa.UUID(), nullable=False),
        sa.Column("friend_id", sa.UUID(), nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["friend_id"],
            ["profiles.uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.uuid"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint(
            "profile_id", "friend_id", name="idx_unique_profile_friend"
        ),
    )
    op.create_table(
        "posts",
        sa.Column("header", sa.String(length=50), nullable=False),
        sa.Column("hashtag", sa.String(length=30), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("likes", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.UUID(), nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.uuid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("profile_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("posts")
    op.drop_table("friends")
    op.drop_table("profiles")
    # ### end Alembic commands ###
