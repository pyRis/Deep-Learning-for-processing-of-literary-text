
search_dir=data/DE/test/*
for dir in $search_dir; do
    echo "Inference on play $dir"
    out_file="$(basename $dir)"
    python3 code/inference.py --input_path $dir --model models/ --output_path $out_file
done