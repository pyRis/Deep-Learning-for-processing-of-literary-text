
search_dir=$1 #data/DE/test/*
out_dir=$2 #"summary/DE/finetuned/"
models="models/mBart-custom-only  models/mBart-jointly  models/mBart-samsum-only  models/mt5-custom-only  models/mt5-jointly  models/mt5-samsum-only"
src_lang=$3
tgt_lang=$4
for model in $models; do
    for dir in $search_dir/*; do
        echo "Inference on play $dir"
        out_file="$(basename $dir)"
        out_model="$(basename $model)"
        out_path="$out_dir/$out_model/$out_file"
        mkdir -p $out_path
        python3 code/DE/inference.py --input_path $dir --model $model --output_path $out_path --tgt_lang $tgt_lang --src_lang $src_lang
    done
done
