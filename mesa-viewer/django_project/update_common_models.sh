tempfile=common/auto_models.tmp
autofile=common/auto_models.py

echo "# This file is generated automatically from the database by running ../update_common_models.sh." > $tempfile
echo "# Do not manually edit this file because any changes will be lost when a new file is generated." >> $tempfile
echo "# The models can be customized by editing models.py in this directory." >> $tempfile
echo "" >> $tempfile

echo "from django.contrib.auth.models import User as AuthUser" >> $tempfile
echo "" >> $tempfile

python inspectdb.py default organisation >> $tempfile
python inspectdb.py default user_profile >> $tempfile

# Inspectdb does not output Postgres Serial type correctly so rather let Django handle the id field
sed  /\ id\ .*=.*IntegerField.*primary_key=True/d $tempfile > $autofile

rm $tempfile

