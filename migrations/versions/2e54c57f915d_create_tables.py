"""create tables

Revision ID: 2e54c57f915d
Revises: 
Create Date: 2019-07-03 14:07:35.022724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e54c57f915d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('review_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('repo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('repository', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('topic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=64), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('last_study_date', sa.DateTime(), nullable=True),
    sa.Column('start_skill', sa.Float(), nullable=True),
    sa.Column('current_skill', sa.Float(), nullable=True),
    sa.Column('mastery', sa.Integer(), nullable=True),
    sa.Column('repo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['repo_id'], ['repo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_topic_created_date'), 'topic', ['created_date'], unique=False)
    op.create_index(op.f('ix_topic_current_skill'), 'topic', ['current_skill'], unique=False)
    op.create_index(op.f('ix_topic_filename'), 'topic', ['filename'], unique=False)
    op.create_index(op.f('ix_topic_last_study_date'), 'topic', ['last_study_date'], unique=False)
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('review_date', sa.DateTime(), nullable=True),
    sa.Column('time_spent', sa.Integer(), nullable=True),
    sa.Column('skill_before', sa.Float(), nullable=True),
    sa.Column('skill_after', sa.Float(), nullable=True),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_review_date'), 'review', ['review_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_review_review_date'), table_name='review')
    op.drop_table('review')
    op.drop_index(op.f('ix_topic_last_study_date'), table_name='topic')
    op.drop_index(op.f('ix_topic_filename'), table_name='topic')
    op.drop_index(op.f('ix_topic_current_skill'), table_name='topic')
    op.drop_index(op.f('ix_topic_created_date'), table_name='topic')
    op.drop_table('topic')
    op.drop_table('repo')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
