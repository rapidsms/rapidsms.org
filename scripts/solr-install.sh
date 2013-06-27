if [ ! -d ./apache-solr-3.6.2 ]
then
    wget http://apache.mirrors.tds.net/lucene/solr/3.6.2/apache-solr-3.6.2.tgz
    tar xvzf apache-solr-3.6.2.tgz
    rm apache-solr-3.6.2.tgz
fi
if [ ! -d ./apache-solr-3.6.2/website ]
then
    cp -r ./apache-solr-3.6.2/example ./apache-solr-3.6.2/website/
fi
ln -sf $PWD/conf/local/project/solr/solrconfig.xml ./apache-solr-3.6.2/website/solr/conf/solrconfig.xml
ln -sf $PWD/conf/local/project/solr/schema.xml ./apache-solr-3.6.2/website/solr/conf/schema.xml
