# https://github.com/toastdriven/django-haystack/pull/706
schema='conf/solr/schema.xml'
cd ../
python manage.py build_solr_schema > $schema
sed -i 's/words=\"stopwords_en.txt\"/words=\"lang\/stopwords_en.txt\"/' $schema
