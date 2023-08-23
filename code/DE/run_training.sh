python3 run_summarization.py --model_name_or_path facebook/mbart-large-cc25 --lang de_DE --do_train --do_eval --train_file joint_data/train.csv --validation_file joint_data/validation.csv --test_file joint_data/test.csv --output_dir  models_new --save_strategy steps --save_steps 5000 --save_total_limit 3 --per_device_train_batch_size=4 --per_device_eval_batch_size=4




