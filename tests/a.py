from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
from datasets import load_dataset
import os
import numpy as np
from sklearn.metrics import accuracy_score
import scipy.special

os.environ["WANDB_MODE"] = "disabled"

# 模型的本地路径
model_path = "/home/fjy/folders/ERNIE2.0/checkpoints/bert-base-chinese"

# 加载分词器和分类模型
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=5)

# 检查是否有可用的 GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 加载自定义的数据集
data_files = {"train": "/home/fjy/folders/ERNIE2.0/trm.json", "validation": "/home/fjy/folders/ERNIE2.0/vrm.json","test": "/home/fjy/folders/ERNIE2.0/tet.json"}
dataset = load_dataset("json", data_files=data_files)

# 定义数据处理函数
def preprocess_function(examples):
    inputs = [f"{prompt} {chosen}" for prompt, chosen in zip(examples["prompt"], examples["chosen"])]
    model_inputs = tokenizer(inputs, max_length=100, truncation=True, padding=True, return_tensors="pt")
    model_inputs["labels"] = examples["label"]
    return model_inputs

# 应用数据处理
encoded_dataset = dataset.map(preprocess_function, batched=True)

# 训练设置
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=50,
    weight_decay=0.01,
)

# 使用 Trainer 进行训练
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["validation"],  # 提供评估数据集
)

# 训练模型
trainer.train()

#  # 定义用于评分的输入
# prompt = "请以你的方式向我描述你的日常生活。"
# response = "草原辽阔，牛羊成群，清晨总是伴随着马蹄声开始。"
# input_text = f"{prompt} {response}"

# # 编码输入
# inputs = tokenizer(input_text, return_tensors="pt").to(device)

#  # 进行推理，得到预测概率
# model.eval()
# with torch.no_grad():
#     outputs = model(**inputs)
#     probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
#     scores = probabilities.cpu().numpy()

# print(f"唐、宋、元等朝代的预测概率: {scores}")

# 从测试集中取到数据。
subset_dataset = encoded_dataset["test"]

# 使用 trainer.predict() 进行预测
predictions_output = trainer.predict(subset_dataset)

# # 获取预测的标签和真实标签
# predicted_labels = np.argmax(predictions_output.predictions, axis=1)
true_labels = predictions_output.label_ids
predictions = predictions_output.predictions

probabilities = scipy.special.softmax(predictions, axis=1)

# # 计算准确率
# accuracy = accuracy_score(true_labels, predicted_labels)
# print(f"Accuracy on that samples: {accuracy}")

# # 输出评估指标
# print(predictions_output.metrics)

sorted_indices_desc = np.argsort(-predictions, axis=1)
top_two_indices = sorted_indices_desc[:, :2]  # 获取前两个索引

# 获取对应的预测分数
# top_two_scores = np.take_along_axis(predictions, top_two_indices, axis=1)
top_two_probabilities = np.take_along_axis(probabilities, top_two_indices, axis=1)

# 打印结果
# print("Top two predicted class indices for each sample:")
# print(top_two_indices)

print("Corresponding prediction scores:")
print(top_two_probabilities)

correct_top2 = [true_label in top_indices for true_label, top_indices in zip(true_labels, top_two_indices)]
top2_accuracy = np.mean(correct_top2)
print(f"Top-2 Accuracy: {top2_accuracy}")

# 保存模型和分词器
save_directory = "/home/fjy/folders/ERNIE2.0/checkpoints/bert_reward1"
trainer.save_model(save_directory)
tokenizer.save_pretrained(save_directory)