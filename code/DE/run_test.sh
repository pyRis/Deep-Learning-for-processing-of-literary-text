
search_dir=$1 #data/DE/test/*
out_dir=$2 #"summary/DE/finetuned/"
model=$3
src_lang=$4
tgt_lang=$5
for dir in $search_dir; do
    echo "Inference on play $dir"
    out_file="$(basename $dir)"
    out_path="$out_dir/$out_file"
    mkdir -p $out_path
    python3 code/DE/inference.py --input_path $dir --model $model --output_path $out_path --tgt_lang $tgt_lang --src_lang $src_lang
done
