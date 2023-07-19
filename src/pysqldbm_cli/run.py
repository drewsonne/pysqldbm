import click

from pysqldbm import Client


@click.group()
@click.option("--api-key", "-k", envvar="SQLDBM_API_KEY")
@click.pass_context
def run(ctx: click.Context, api_key: str):
    ctx.obj = Client(api_key)


@run.group()
@click.pass_context
def projects(ctx: click.Context):
    pass


@projects.command("list")
@click.pass_obj
def list_projects(client: Client):
    for project in client.projects.list():
        click.echo(f"{project.id} {project.name}")


@projects.command()
@click.argument("project_id")
@click.pass_obj
def get(client: Client, project_id: str):
    project = client.projects.get(project_id)
    click.echo(f"{project.id} {project.name}")


if __name__ == "__main__":
    run()
