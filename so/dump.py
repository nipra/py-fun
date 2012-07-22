# Copied from: http://meta.stackoverflow.com/questions/28103/python-script-to-import-create-sqlite3-database-from-so-data-dump
# With some minor changes.
import sqlite3
import os
import xml.etree.cElementTree as etree
import logging
import pprint

ANATHOMY = {
    'badges': {
        'Id':'INTEGER',
        'UserId':'INTEGER',
        'Name':'TEXT',
        'Date':'DATETIME',
        },
    'comments': {
        'Id':'INTEGER',
        'PostId':'INTEGER',
        'Score':'INTEGER',
        'Text':'TEXT',
        'CreationDate':'DATETIME',
        'UserId':'INTEGER',
        },
    'posts': {
        'Id':'INTEGER', 
        'PostTypeId':'INTEGER', # 1: Question, 2: Answer
        'ParentID':'INTEGER', # (only present if PostTypeId is 2)
        'AcceptedAnswerId':'INTEGER', # (only present if PostTypeId is 1)
        'CreationDate':'DATETIME',
        'Score':'INTEGER',
        'ViewCount':'INTEGER',
        'Body':'TEXT',
        'OwnerUserId':'INTEGER', # (present only if user has not been deleted) 
        'LastEditorUserId':'INTEGER',
        'LastEditorDisplayName':'TEXT', #="Rich B" 
        'LastEditDate':'DATETIME', #="2009-03-05T22:28:34.823" 
        'LastActivityDate':'DATETIME', #="2009-03-11T12:51:01.480" 
        'CommunityOwnedDate':'DATETIME', #(present only if post is community wikied)
        'Title':'TEXT',
        'Tags':'TEXT',
        'AnswerCount':'INTEGER',
        'CommentCount':'INTEGER',
        'FavoriteCount':'INTEGER',
        'ClosedDate':'DATETIME',
        },
    'votes': {
        'Id':'INTEGER',
        'PostId':'INTEGER',
        'UserId':'INTEGER',
        'VoteTypeId':'INTEGER',
        # -   1: AcceptedByOriginator
        # -   2: UpMod
        # -   3: DownMod
        # -   4: Offensive
        # -   5: Favorite
        # -   6: Close
        # -   7: Reopen
        # -   8: BountyStart
        # -   9: BountyClose
        # -  10: Deletion
        # -  11: Undeletion
        # -  12: Spam
        # -  13: InformModerator
        'CreationDate':'DATETIME',
        'BountyAmount':'INTEGER'
        },
    'users': {
        'Id':'INTEGER',
        'Reputation':'INTEGER',
        'CreationDate':'DATETIME',
        'DisplayName':'TEXT',
        'LastAccessDate':'DATETIME',
        'WebsiteUrl':'TEXT',
        'Location':'TEXT',
        'Age':'INTEGER',
        'AboutMe':'TEXT',
        'Views':'INTEGER',
        'UpVotes':'INTEGER',
        'DownVotes':'INTEGER',
        'EmailHash':'TEXT'
        },
    }

BASE_DUMP_PATH = '/home/nipra/Data/Stack Overflow Data Dump - Jan 2011/Content/'

DUMP_PATHS = ['012011 Ask Ubuntu/',
              '012011 Ask Ubuntu Meta/',
              '012011 Cooking/',
              '012011 Cooking Meta/',
              '012011 English Language and Usage/',
              '012011 English Language and Usage Meta/',
              '012011 Game Development/',
              '012011 Game Development Meta/',
              '012011 Gaming/',
              '012011 Gaming Meta/',
              '012011 Mathematics/',
              '012011 Mathematics Meta/',
              '012011 Meta Server Fault/',
              '012011 Meta Stack Overflow/',
              '012011 Meta Super User/',
              '012011 Photography/',
              '012011 Photography Meta/',
              '012011 Programmers/',
              '012011 Programmers Meta/',
              '012011 Server Fault/',
              '012011 Stack Apps/',
              '012011 Statistical Analysis/',
              '012011 Statistical Analysis Meta/',
              '012011 Super User/',
              '012011 TeX - LaTeX/',
              '012011 TeX - LaTeX Meta/',
              '012011 Theoretical Computer Science/',
              '012011 Theoretical Computer Science Meta/',
              '012011 Web Applications/',
              '012011 Web Applications Meta/',
              '012011 Webmasters/',
              '012011 Webmasters Meta/',]

def get_dump_paths(base_dump_path=BASE_DUMP_PATH, dump_paths=DUMP_PATHS):
    paths = [(BASE_DUMP_PATH + path) for path in DUMP_PATHS]
    paths.append(BASE_DUMP_PATH)
    return paths
    
def dump_files(file_names, anathomy, 
               dump_path='', 
               dump_database_name = 'so-dump.db',
               create_query='CREATE TABLE IF NOT EXISTS [{table}]({fields})',
               insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
               log_filename='so-parser.log',
               db_path='/home/nipra/sqlite/'):

    logging.basicConfig(filename=os.path.join(dump_path, log_filename),level=logging.INFO)
    db = sqlite3.connect(os.path.join(db_path, dump_database_name))

    for file in file_names:
        print "Opening {0}.xml".format(file)
        with open(os.path.join(dump_path, file + '.xml')) as xml_file:
            tree = etree.iterparse(xml_file)
            table_name = file

            sql_create = create_query.format(
                table=table_name, 
                fields=", ".join(['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))
            print('Creating table {0}'.format(table_name))

            try:
                logging.info(sql_create)
                db.execute(sql_create)
            except Exception, e:
                logging.warning(e)

            for events, row in tree:
                try:
                    logging.debug(row.attrib.keys())

                    db.execute(insert_query.format(
                            table=table_name, 
                            columns=', '.join(row.attrib.keys()), 
                            values=('?, ' * len(row.attrib.keys()))[:-2]),
                               row.attrib.values())
                    print ".",
                except Exception, e:
                    logging.warning(e)
                    print "x",
                finally:
                    row.clear()
            print "\n"
            db.commit()
            del(tree)

if __name__ == '__main__':
    for dump_path in get_dump_paths():
        dump_files(ANATHOMY.keys(), ANATHOMY, dump_path)
