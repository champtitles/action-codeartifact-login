import os
from os.path import expanduser
import xml.etree.ElementTree

MAVEN_REPO_ID = os.environ['MAVEN_REPO_ID']
MAVEN_REPO_URL = os.environ['MAVEN_REPO_URL']
CODEARTIFACT_AUTH_TOKEN = os.environ['CODEARTIFACT_AUTH_TOKEN']

settings_path = os.path.join(expanduser("~"), '.m2', 'settings.xml')
settings_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<settings>
    <servers>
        <server>
            <id>{MAVEN_REPO_ID}</id>
            <username>aws</username>
            <password></password>
        </server>
    </servers>
    <profiles>
        <profile>
            <id>{MAVEN_REPO_ID}</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <repositories>
                <repository>
                    <id>{MAVEN_REPO_ID}</id>
                    <url>{MAVEN_REPO_URL}</url>
                </repository>
            </repositories>
        </profile>
    </profiles>
</settings>'''


print(f'Writing settings file: {settings_path}')
with open(settings_path, 'w') as f:
    f.write(settings_template)

print(f'Updating AWS token in settings file: {settings_path}')
et = xml.etree.ElementTree.parse(settings_path)
for elem in et.findall('servers'):
    for server in elem.findall('server'):
        for server_id in server.findall('id'):
            if server_id.text == MAVEN_REPO_ID:
                for password in server.findall('password'):
                    password.text = CODEARTIFACT_AUTH_TOKEN

et.write(settings_path)
print(f'{settings_path} has been updated')
