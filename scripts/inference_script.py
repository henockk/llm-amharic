import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv('API_TOKEN')


from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

login(api_token)

# Load the tokenizer and model with quantization
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    load_in_8bit=True,  # Use 8-bit quantization
    device_map="auto"   # Automatically map model to available devices (GPU)
)

# Generate text inference test
input_text_amharic = "ሰላም እንደት ዋልክ?"
inputs_amharic = tokenizer(input_text_amharic, return_tensors="pt").to("cuda")

# Generate text
outputs_amharic = model.generate(**inputs_amharic)
generated_text_amharic = tokenizer.decode(outputs_amharic[0], skip_special_tokens=True)
print("Generated Text:", generated_text_amharic)


# Question answer inference
question_amharic = "ኢትዮጵያ የት ነው?"
inputs_question = tokenizer(question_amharic, return_tensors="pt").to("cuda")

# Generate answer
outputs_answer = model.generate(**inputs_question)
answer_amharic = tokenizer.decode(outputs_answer[0], skip_special_tokens=True)
print("Answer:", answer_amharic)


# News classification inference
news_classification = ""
inputs_question = tokenizer(news_classification, return_tensors="pt").to("cuda")

# Generate answer
outputs_answer = model.generate(**inputs_question)
answer_amharic = tokenizer.decode(outputs_answer[0], skip_special_tokens=True)
print("Answer:", answer_amharic)



# Summarize text infernce test
input_text = """
በሕወትህ በአንድ ባመንክበትና ትክክል በሆነ ዓላማ እስከመጨረሻው ከመጽናት ውጪ ምንም ቁም ነገር ልታከናውን አትችልም፡፡ 
ዛሬ ይህንና ያንን እየጀመርክ እስከጥጉ ሳታደርሳቸው ነገ ደግሞ ወደሌላ ነገር ዘወር የማለት ለማድ ካለህ በተቻለህ ፍጥነት ይህንን ዘይቤ መቀየር እንዳለብህ ትመከራለህ፡፡ 
አብዛኛውን ጊዜ አንድን የጀመርነውን ነገር እስከጥጉ የማንወስድበት ዋነኛ ምክንያት ስንወድቅ ወይም ያልተሳካልን ሲመስለን ነው፡፡ ሆኖም፣ ውድቀት፣ አለመሳካት፣ እንቅፋትና
የመሳሰሉት ሁኔታዎች በማንኛውም አንድን መልካም አላማ ይዞ በሚራመድ ሰው ሕይወት ውስጥ የማይቀሩ ሂደቶች ናቸው፡፡ 
ስለዚህም፣ አንደኛችንን ውድቀትን አያያዝ ብልሃት ማዳበር አስፈላጊ ነው፡፡"""

inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding="max_length", max_length=1024).to("cuda")

# Summarize text
summary_outputs = model.generate(**inputs)
summary_text = tokenizer.decode(summary_outputs[0], skip_special_tokens=True)
print(summary_text)
