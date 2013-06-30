{% import 'project/_vars.sls' as vars with context %}
{% set venv_dir = vars.path_from_root('env') %}

include:
  - memcached
  - postfix
  - version-control
  - python
  - supervisor

root_dir:
  file.directory:
    - name: {{ vars.root_dir }}
    - user: {{ pillar['project_name'] }}
    - group: admin
    - mode: 775
    - makedirs: True
    - require:
      - user: project_user

run_dir:
  file.directory:
    - name: {{ vars.run_dir }}
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - mode: 775
    - makedirs: True
    - require:
      - user: project_user

log_dir:
  file.directory:
    - name: {{ vars.log_dir }}
    - user: {{ pillar['project_name'] }}
    - group: www-data
    - mode: 775
    - makedirs: True
    - require:
      - file: root_dir

venv:
  virtualenv.managed:
    - name: {{ venv_dir }}
    - no_site_packages: True
    - distribute: True
    - require:
      - pip: virtualenv
      - file: root_dir

venv_dir:
  file.directory:
    - name: {{ venv_dir }}
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - recurse:
      - user
      - group
    - require:
      - virtualenv: venv

activate:
  file.append:
    - name: {{ vars.build_path(venv_dir, "bin/activate") }}
    - text: source {{ vars.build_path(venv_dir, "bin/secrets") }}
    - require:
      - virtualenv: venv

secrets:
  file.managed:
    - name: {{ vars.build_path(venv_dir, "bin/secrets") }}
    - source: salt://project/env_secrets.jinja2
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - template: jinja
    - require:
      - file: activate

group_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/{{ vars.project }}-group.conf
    - source: salt://project/supervisor/group.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        programs: "{{ vars.project }}-server"
        project: "{{ vars.project }}"
    - require:
      - pkg: supervisor
      - file: log_dir
    - watch_in:
      - cmd: supervisor_update

gunicorn_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/{{ vars.project }}-gunicorn.conf
    - source: salt://project/supervisor/gunicorn.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        log_dir: "{{ vars.log_dir }}"
        virtualenv_root: "{{ venv_dir }}"
        settings: "{{ pillar['project_name']}}.settings.{{ pillar['environment'] }}"
        project: "{{ vars.project }}"
        socket: "{{ vars.server_socket }}"
    - require:
      - pkg: supervisor
      - file: log_dir
    - watch_in:
      - cmd: supervisor_update

gunicorn_process:
  supervisord:
    - name: {{ vars.project }}:{{ vars.project }}-server
    - running
    - restart: True
    - update: True
    - require:
      - pkg: supervisor
      - file: group_conf
      - file: gunicorn_conf

npm:
  pkg:
    - installed

less:
  cmd.run:
    - name: npm install less@1.3.3 -g
    - user: root
    - unless: which lessc
    - require:
      - pkg: npm
  file.symlink:
    - name: /usr/bin/lessc
    - target: /usr/local/bin/lessc


# openjdk-7-jre-headless:
#   pkg:
#     - installed

# solr_conf:
#   file.managed:
#     - name: /etc/supervisor/conf.d/{{ pillar['project_name'] }}-solr.conf
#     - source: salt://project/supervisor/solr.conf
#     - user: root
#     - group: root
#     - mode: 644
#     - template: jinja
#     - context:
#         log_dir: "/var/www/{{ pillar['project_name']}}/log"
#     - require:
#       - pkg: openjdk-7-jre-headless
#       - file: log_dir

# solr:
#   cmd.script:
#     - cwd: /var/www/{{ pillar['project_name']}}
#     - name: salt://project/solr-install.sh
#     - runas: {{ pillar['project_name'] }}


# /var/www/{{ pillar['project_name']}}/solr-run.sh:
#     file.managed:
#       - source: salt://project/solr-run.sh
#       - user: website
#       - group: admin
#       - mode: 775

# /var/www/{{ pillar['project_name']}}/apache-solr-3.6.2/website:
#     file.directory:
#     - user: website
#     - group: admin
#     - dir_mode: 755
#     - recurse:
#         - user
#         - group
#         - mode

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

# extend:
#   supervisor:
#     service:
#       - running
#       - watch:
#         - file: group_conf
#         - file: gunicorn_conf
#         - file: solr_conf
