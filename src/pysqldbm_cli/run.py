import json
from types import GeneratorType
from typing import Union, Dict, List, Generator
from packaging.version import Version

import click

import pysqldbm
from pysqldbm.client import Client
from pysqldbm_cli.build import bump_version, get_branch_type


@click.group()
@click.option("--api-key", "-k", envvar="SQLDBM_API_KEY")
@click.pass_context
def run(ctx: click.Context, api_key: str):
    ctx.obj = pysqldbm.client(api_key)


@run.command("list-projects")
@click.pass_obj
def list_projects(client: Client):
    print_json(client.list_projects())


@run.command("get-project")
@click.option("--id", "id_", type=int, required=True)
@click.pass_obj
def get(client: Client, id_: str):
    for project in client.list_projects():
        if project["id"] == id_:
            print_json(project)
            break


# Revisions
@run.command("list-revisions")
@click.option("--project-id", type=int, required=True)
@click.pass_obj
def list_revisions(client: Client, project_id: str):
    print_json(client.list_revisions(project_id))


@run.command("get-revision")
@click.option("--project-id", type=int, required=True)
@click.option("--revision-id", type=int, required=True)
@click.pass_obj
def get_revisions(client: Client, project_id: str, revision_id: str):
    print_json(client.get_revision(project_id, revision_id))


@run.command("get-last-revision")
@click.option("--project-id", type=int, required=True)
@click.pass_obj
def get_last_revisions(client: Client, project_id: str):
    print_json(client.get_last_revision(project_id))


@run.command("get-ddl")
@click.option("--project-id", type=int, required=True)
@click.option("--revision-id", type=int, required=True)
@click.pass_obj
def get_ddl(client: Client, project_id: str, revision_id: str):
    print_json(client.get_ddl(project_id, revision_id))


@run.command("get-last-ddl")
@click.option("--project-id", type=int, required=True)
@click.pass_obj
def get_last_ddl(client: Client, project_id: str):
    print_json(client.get_last_ddl(project_id))


@run.command("list-environments")
@click.option("--project-id", type=int, required=True)
@click.pass_obj
def list_environments(client: Client, project_id: str):
    print_json(client.list_environments(project_id))


@run.command("get-latest-alter-statement")
@click.option("--project-id", type=int, required=True)
@click.option("--raw/--no-raw", default=False)
@click.pass_obj
def get_latest_alter_statement(client: Client, project_id: str, raw: bool):
    statement = client.get_latest_alter_statement(project_id)
    if raw:
        click.echo(statement)
    else:
        print_json({"statement": statement})


@run.command("get-alter-statement")
@click.option("--project-id", type=int, required=True)
@click.option("--revision-id", type=int, required=True)
@click.option("--environment-id", type=int, required=True)
@click.option("--with-revision-id", type=int, required=True)
@click.option("--with-environment-id", type=int, required=True)
@click.option("--raw/--no-raw", default=False)
@click.pass_obj
def get_alter_statement(
    client: Client,
    project_id: str,
    revision_id: str,
    environment_id: str,
    with_revision_id: str,
    with_environment_id: str,
    raw: bool,
):
    statement = client.get_alter_statement(
        project_id, revision_id, environment_id, with_revision_id, with_environment_id
    )
    if raw:
        click.echo(statement)
    else:
        print_json({"statement": statement})


@run.command("get-latest-object-ddl")
@click.option("--project-id", type=int, required=True)
@click.option("--object-name", type=str, required=True)
@click.option("--case-sensitive", is_flag=True, default=False)
@click.option("--raw/--no-raw", default=False)
@click.pass_obj
def get_latest_object_ddl(client: Client, project_id: str, object_name: str, case_sensitive: bool, raw: bool):
    statement = client.get_latest_object_ddl(project_id, object_name, case_sensitive)
    if raw:
        click.echo(statement)
    else:
        print_json({"statement": statement})


@run.command("get-object-ddl")
@click.option("--project-id", type=int, required=True)
@click.option("--revision-id", type=int, required=True)
@click.option("--object-name", type=str, required=True)
@click.option("--case-sensitive", is_flag=True, default=False)
@click.option("--raw/--no-raw", default=False)
@click.pass_obj
def get_object_ddl(
    client: Client,
    project_id: str,
    revision_id,
    object_name: str,
    case_sensitive: bool,
    raw: bool,
):
    statement = client.get_object_ddl(project_id, revision_id, object_name, case_sensitive)
    if raw:
        click.echo(statement)
    else:
        print_json({"statement": statement})


# Add hidden build commands
@run.group("build", hidden=True)
def build(): ...


@build.command("version-bump")
@click.option("-B", "--branch", help="Branch name", required=True)
@click.option("-b", "--build", help="Build number", type=int)
@click.option("-p", "--pr", help="Pull Request number", type=int)
@click.option("-t", "--tag", help="Tag version", type=str, default=None)
@click.option("-c", "--current-version", help="Current version", required=True)
@click.option(
    "-l",
    "--latest-release",
    default=None,
    help="Latest release version",
    required=True,
)
def version_bump(
    branch: str,
    build: int,
    pr: int,
    tag: str | None,
    latest_release: str,
    current_version: str,
):
    click.echo(
        bump_version(
            get_branch_type(branch),
            tag,
            build,
            pr,
            Version(latest_release),
            Version(current_version),
        )
    )


def print_json(obj: Union[Dict, List[Dict], Generator[Dict, None, None]]):
    """
    Print a JSON object to the console with syntax highlighting.

    Args:
        obj (Union[Dict, List[Dict], Generator[Dict, None, None]]): The JSON object to print.
            This can be a dictionary, a list of dictionaries, or a generator of dictionaries.

    Returns:
        None
    """
    if isinstance(obj, GeneratorType):
        obj = [o for o in obj]

    """Prints a JSON object to the console with syntax highlighting."""
    click.echo(click.style(json.dumps(obj, indent=2, sort_keys=True), fg="green"))


if __name__ == "__main__":
    run()
