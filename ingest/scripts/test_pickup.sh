#!/bin/bash

target_dir=$1

touch moved.file
touch /tmp/copied.file

touch $target_dir/touched.file
mv moved.file $target_dir
cp /tmp/copied.file $target_dir
echo 'text' > $target_dir/text.file
touch $target_dir/touched.file
echo 'more text' >> $target_dir/text.file

sleep 1

ls -lah $target_dir


