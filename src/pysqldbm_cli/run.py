import click

from pysqldbm import Client
from pysqldbm.resources.revisions import Revision


@click.group()
@click.option("--api-key", "-k", envvar="SQLDBM_API_KEY")
@click.pass_context
def run(ctx: click.Context, api_key: str):
    ctx.obj = Client(api_key)


## Projects
@run.command("list-projects")
@click.pass_obj
def list_projects(client: Client):
    for project in client.projects.list():
        click.echo(f"{project.id} {project.name}")


@run.command("get-project")
@click.option("--project-id")
@click.pass_obj
def get(client: Client, project_id: str):
    project = client.projects.get(project_id)
    click.echo(f"{project.id} {project.name}")


# Revisions
@run.command("get-revision")
@click.option("--project-id")
@click.option("--revision-id")
@click.pass_obj
def get(client: Client, project_id: str, revision_id: str):
    rev = Revision(client, project_id, revision_id).fetch()


if __name__ == "__main__":
    run()
