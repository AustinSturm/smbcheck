#!/usr/bin/env python2
from impacket.smbconnection import SMBConnection, smb
import click


@click.command()
@click.option('--host', '-h')
@click.option('--file', '-f', type=click.Path(exists=True))
def check_smbv1(host, file):
    if not host and not file:
        return

    if host:
        hosts = [host]
    if file:
        with open(file) as f:
            hosts = f.read().splitlines()

    for target in hosts:
        click.echo('Attempting SMBv1 negotation with {}...\t'.format(target), nl=False)
        try:
            s = SMBConnection('*SMBSERVER', target, preferredDialect=smb.SMB_DIALECT)
            if isinstance(s, SMBConnection):
                click.secho('Success', fg='green')
                ## broken
                try:
                    click.echo('\t- Dialect: {}...\t'.format(smb.SMB_DIALECT), nl=True)
                    s.login("", "")
                    click.echo('\t- OS: {}'.format(s.getServerOS()), nl=True)
                    click.echo('\t- Shares:', nl=True)
                    # attempt null session to enumerate shares
                    shares = s.listShares()
                    for share in shares:
                        click.echo('\t\t- {}'.format(share['shi1_netname']), nl=True)
                except Exception:
                    pass

        except Exception as e:
            click.secho('Failed\t', fg='red', nl=False)
            click.echo(e)
            pass

if __name__ == '__main__':
        check_smbv1()
