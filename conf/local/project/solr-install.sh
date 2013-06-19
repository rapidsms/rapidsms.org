cd /usr/local
if [ ! -d ./apache-solr-3.6.2 ]
then
    wget http://apache.mirrors.tds.net/lucene/solr/3.6.2/apache-solr-3.6.2.tgz
    tar xvzf apache-solr-3.6.2.tgz
    rm apache-solr-3.6.2.tgz
fi
if [ ! -d ./apache-solr-3.6.2/rapidsms ]
then
    cp -r ./apache-solr-3.6.2/example ./apache-solr-3.6.2/rapidsms/
fi
    ln -sf $PWD/conf/solr/solrconfig.xml ./apache-solr-3.6.2/rapidsms/solr/conf/solrconfig.xml
    ln -sf $PWD/conf/solr/schema.xml ./apache-solr-3.6.2/rapidsms/solr/conf/schema.xml
