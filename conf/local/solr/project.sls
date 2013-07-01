include:
  - solr

solr_install:
  cmd.script:
    - cwd: /var/www/{{ pillar['project_name']}}-{{ pillar['environment']}}
    - name: salt://solr/solr-install.sh
    - user: {{ pillar['project_name'] }}

solr_website:
    file.directory:
    - name: /var/www/{{ pillar['project_name']}}-{{ pillar['environment']}}/apache-solr-3.6.2/website
    - user: {{ pillar['project_name'] }}
    - group: admin
    - dir_mode: 775
    - recurse:
        - user
        - group
        - mode
    - require:
      - group: admin
      - cmd: solr_install


# /var/www/{{ pillar['project_name']}}/solr-run.sh:
#     file.managed:
#       - source: salt://project/solr-run.sh
#       - user: website
#       - group: admin
#       - mode: 775



# /var/www/{{ pillar['project_name']}}/apache-solr-3.6.2/website/solr/conf/schema.xml:
#   file.managed:
#   - source: salt://project/solr/schema.xml
#   - user: website
#   - group: admin
#   - mode: 775

# /var/www/{{ pillar['project_name']}}/apache-solr-3.6.2/website/solr/conf/solrconfig.xml:
#   file.managed:
#   - source: salt://project/solr/solrconfig.xml
#   - user: website
#   - group: admin
#   - mode: 775
