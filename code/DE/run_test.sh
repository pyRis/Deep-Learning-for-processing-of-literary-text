
search_dir=data/DE/test/*
out_dir="summary/DE/finetuned/"
for dir in $search_dir; do
    echo "Inference on play $dir"
    out_file="$(basename $dir)"
    out_path="$out_dir/$out_file"
    mkdir -p $out_path
    python3 code/DE/inference.py --input_path $dir --model models_new/ --output_path $out_path
done
