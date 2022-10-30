from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in workflow_base_kanban_board_khatavahi/__init__.py
from workflow_base_kanban_board_khatavahi import __version__ as version

setup(
	name="workflow_base_kanban_board_khatavahi",
	version=version,
	description="Create Kanban Board base on Workflow",
	author="Jigar Tarpara",
	author_email="jigartarpara@khatavahi.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
