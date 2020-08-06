#!/bin/bash

# 自身の場所をカレントディレクトリに
MY_DIRNAME=$(dirname $0)
cd $MY_DIRNAME

# 前回zipファイルを削除
rm lambda.zip

# zip化
# functionフォルダ自体を含まずにフォルダ配下をzip化できるように移動
cd lambda/function
zip -r ../../lambda.zip *
