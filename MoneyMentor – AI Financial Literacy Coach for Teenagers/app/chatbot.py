import os
import re # Import the regular expression module for text processing
import asyncio # Import asyncio

# LangChain specific imports
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# --- Configuration and Setup ---
# Set your Google API Key as an environment variable.
os.environ["GOOGLE_API_KEY"] = "Your own Key Not giving you mine ;) " # <<< IMPORTANT: Replace with your actual key

# --- Asyncio Event Loop Handling ---
# Ensure there's an asyncio event loop running for the current thread.
# This is crucial for libraries that rely on asyncio, like parts of langchain_google_genai.
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# --- Data Loading and Vector Store Creation ---
loader = CSVLoader(file_path=r"data\rag_finance_kb.csv", encoding="utf-8")
documents = loader.load()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# --- Gen Z Slang Translation Mapping ---
GENZ_slang_mapping = {
    "important": "low-key crucial", "very good": "on fleek", "understand": "get the vibe",
    "money": "bread", "broke": "down bad", "save": "secure the bag", "good": "bussin'",
    "cool": "rizz", "excellent": "slay", "challenge": "tea", "difficult": "no cap",
    "easy": "chill", "excited": "hyped", "boring": "mid", "surprising": "wild",
    "annoying": "cringe", "relax": "vibe", "smart": "big brain", "confused": "confused af",
    "facts": "facts, no cap", "true": "real talk", "joke": "cap", "lying": "capping",
    "honest": "fr fr", "seriously": "deadass", "awesome": "bet", "agree": "bet",
    "sure": "bet", "yes": "bet", "deal with it": "it is what it is", "amazing": "fire",
    "stressed": "stressed out of my mind", "tired": "donezo", "something new": "new new",
    "old fashioned": "old school", "traditional": "old school", "interesting": "spill the tea",
    "what's up": "what's good", "really": "for real", "actually": "for real", "truth": "the real tea",
    "nothing": "nothin' much", "come on": "nah", "no": "nah", "definitely": "fosho",
    "absolutely": "fosho", "let's go": "bet", "awesome": "slay", "impressive": "slay",
    "do it well": "slay", "fantastic": "slay", "great": "slay", "terrible": "oof",
    "disappointment": "oof", "sad": "oof", "embarrassing": "oof", "bad": "oof",
    "awkward": "cringe", "embarrassing": "cringe", "uncomfortable": "cringe", "lame": "cringe",
    "uncool": "cringe", "very": "mad", "extremely": "mad", "a lot": "mad", "super": "mad",
    "really": "mad", "hungry": "hangry", "angry": "hangry", "excited": "hype",
    "energetic": "hype", "thrilled": "hype", "good mood": "hype", "relaxed": "chillin'",
    "calm": "chillin'", "doing nothing": "chillin'", "hanging out": "chillin'", "fun": "lit",
    "exciting": "lit", "amazing": "lit", "cool": "lit", "party": "lit", "something good": "a whole vibe",
    "atmosphere": "a whole vibe", "feeling": "a whole vibe", "experience": "a whole vibe",
    "relaxing": "a whole vibe", "enjoyable": "a whole vibe", "easy to understand": "it hits different",
    "unique": "it hits different", "special": "it hits different", "stands out": "it hits different",
    "different": "it hits different", "surprising": "it hits different", "unexpected": "it hits different",
    "good news": "spill the tea", "gossip": "spill the tea", "tell me everything": "spill the tea",
    "what happened": "spill the tea", "speak your mind": "spill the tea", "tell me something interesting": "spill the tea",
    "tell me a secret": "spill the tea", "true story": "no cap", "serious": "no cap",
    "real talk": "no cap", "i'm not lying": "no cap", "believe me": "no cap", "honestly": "no cap",
    "honestly, no kidding": "no cap", "it's true": "no cap", "it's real": "no cap",
    "genuine": "no cap", "authentic": "no cap", "trust me": "no cap", "for real": "no cap",
    "sarcastic": "sarcasm", "ironic": "sarcasm", "playful": "sarcasm", "joking": "sarcasm",
    "not serious": "sarcasm", "not literal": "sarcasm", "lighthearted": "sarcasm", "witty": "sarcasm",
    "clever": "sarcasm", "funny": "sarcasm", "humorous": "sarcasm", "teasing": "sarcasm",
    "mocking": "sarcasm", "derisive": "sarcasm", "sneering": "sarcasm", "cynical": "sarcasm",
    "skeptical": "sarcasm", "distrustful": "sarcasm", "suspicious": "sarcasm", "wary": "sarcasm",
    "cautious": "sarcasm", "circumspect": "sarcasm", "prudent": "sarcasm", "sensible": "sarcasm",
    "wise": "sarcasm", "judicious": "sarcasm", "discreet": "sarcasm", "tactful": "sarcasm",
    "diplomatic": "sarcasm", "polite": "sarcasm", "courteous": "sarcasm", "gracious": "sarcasm",
    "charming": "sarcasm", "engaging": "sarcasm", "winning": "sarcasm", "captivating": "sarcasm",
    "alluring": "sarcasm", "seductive": "sarcasm", "tempting": "sarcasm", "enticing": "sarcasm",
    "inviting": "sarcasm", "attractive": "sarcasm", "appealing": "sarcasm", "desirable": "sarcasm",
    "coveted": "sarcasm", "envied": "sarcasm", "longed for": "sarcasm", "wished for": "sarcasm",
    "dreamed of": "sarcasm", "hoped for": "sarcasm", "aspired to": "sarcasm", "sought after": "sarcasm",
    "pursued": "sarcasm", "chased": "sarcasm", "hunted": "sarcasm", "stalked": "sarcasm",
    "tracked": "sarcasm", "followed": "sarcasm", "trailed": "sarcasm", "shadowed": "sarcasm",
    "dogged": "sarcasm", "persistent": "sarcasm", "determined": "sarcasm", "resolute": "sarcasm",
    "steadfast": "sarcasm", "unwavering": "sarcasm", "unyielding": "sarcasm", "adamant": "sarcasm",
    "firm": "sarcasm", "resolute": "sarcasm", "decisive": "sarcasm", "strong-willed": "sarcasm",
    "stubborn": "sarcasm", "obstinate": "sarcasm", "inflexible": "sarcasm", "uncompromising": "sarcasm",
    "unbending": "sarcasm", "rigid": "sarcasm", "stiff": "sarcasm", "hard": "sarcasm",
    "tough": "sarcasm", "resilient": "sarcasm", "durable": "sarcasm", "sturdy": "sarcasm",
    "robust": "sarcasm", "solid": "sarcasm", "firm": "sarcasm", "compact": "sarcasm",
    "dense": "sarcasm", "thick": "sarcasm", "bulky": "sarcasm", "heavy": "sarcasm",
    "massive": "sarcasm", "huge": "sarcasm", "enormous": "sarcasm", "gigantic": "sarcasm",
    "colossal": "sarcasm", "immense": "sarcasm", "vast": "sarcasm", "broad": "sarcasm",
    "wide": "sarcasm", "spacious": "sarcasm", "ample": "sarcasm", "generous": "sarcasm",
    "abundant": "sarcasm", "plentiful": "sarcasm", "copious": "sarcasm", "profuse": "sarcasm",
    "lavish": "sarcasm", "extravagant": "sarcasm", "luxurious": "sarcasm", "opulent": "sarcasm",
    "rich": "sarcasm", "wealthy": "sarcasm", "affluent": "sarcasm", "prosperous": "sarcasm",
    "flourishing": "sarcasm", "thriving": "sarcasm", "successful": "sarcasm", "victorious": "sarcasm",
    "triumphant": "sarcasm", "conquering": "sarcasm", "dominant": "sarcasm", "supreme": "sarcasm",
    "paramount": "sarcasm", "foremost": "sarcasm", "leading": "sarcasm", "principal": "sarcasm",
    "chief": "sarcasm", "main": "sarcasm", "primary": "sarcasm", "prime": "sarcasm",
    "first": "sarcasm", "original": "sarcasm", "initial": "sarcasm", "earliest": "sarcasm",
    "founding": "sarcasm", "pioneering": "sarcasm", "innovative": "sarcasm", "groundbreaking": "sarcasm",
    "revolutionary": "sarcasm", "transformative": "sarcasm", "radical": "sarcasm",
    "extreme": "sarcasm", "drastic": "sarcasm", "severe": "sarcasm", "harsh": "sarcasm",
    "stern": "sarcasm", "austere": "sarcasm", "rigorous": "sarcasm", "strict": "sarcasm",
    "demanding": "sarcasm", "challenging": "sarcasm", "tough": "sarcasm", "difficult": "sarcasm",
    "arduous": "sarcasm", "laborious": "sarcasm", "onerous": "sarcasm", "burdensome": "sarcasm",
    "cumbersome": "sarcasm", "awkward": "sarcasm", "clumsy": "sarcasm", "ungainly": "sarcasm",
    "unwieldy": "sarcasm", "inelegant": "sarcasm", "graceless": "sarcasm", "cloddish": "sarcasm",
    "loutish": "sarcasm", "boorish": "sarcasm", "uncouth": "sarcasm", "crude": "sarcasm",
    "vulgar": "sarcasm", "coarse": "sarcasm", "gross": "sarcasm", "obscene": "sarcasm",
    "indecent": "sarcasm", "lewd": "sarcasm", "bawdy": "sarcasm", "racy": "sarcasm",
    "suggestive": "sarcasm", "provocative": "sarcasm", "titillating": "sarcasm", "erotic": "sarcasm",
    "sensual": "sarcasm", "sexual": "sarcasm", "lustful": "sarcasm", "lascivious": "sarcasm",
    "wanton": "sarcasm", "immoral": "sarcasm", "sinful": "sarcasm", "wicked": "sarcasm",
    "evil": "sarcasm", "depraved": "sarcasm", "corrupt": "sarcasm", "degenerate": "sarcasm",
    "decadent": "sarcasm", "dissolute": "sarcasm", "profligate": "sarcasm", "licentious": "sarcasm",
    "debauched": "sarcasm", "perverted": "sarcasm", "deviant": "sarcasm", "aberrant": "sarcasm",
    "abnormal": "sarcasm", "unnatural": "sarcasm", "unusual": "sarcasm", "odd": "sarcasm",
    "peculiar": "sarcasm", "queer": "sarcasm", "strange": "sarcasm", "bizarre": "sarcasm",
    "eccentric": "sarcasm", "idiosyncratic": "sarcasm", "quirky": "sarcasm", "unconventional": "sarcasm",
    "unorthodox": "sarcasm", "heretical": "sarcasm", "rebellious": "sarcasm", "insubordinate": "sarcasm",
    "defiant": "sarcasm", "disobedient": "sarcasm", "unruly": "sarcasm", "disruptive": "sarcasm",
    "troublesome": "sarcasm", "annoying": "sarcasm", "irritating": "sarcasm", "exasperating": "sarcasm",
    "frustrating": "sarcasm", "vexing": "sarcasm", "aggravating": "sarcasm", "bothersome": "sarcasm",
    "pesky": "sarcasm", "irksome": "sarcasm", "galling": "sarcasm", "chafing": "sarcasm",
    "rubbing": "sarcasm", "grating": "sarcasm", "jarring": "sarcasm", "harsh": "sarcasm",
    "dissonant": "sarcasm", "cacophonous": "sarcasm", "strident": "sarcasm", "shrill": "sarcasm",
    "piercing": "sarcasm", "loud": "sarcasm", "noisy": "sarcasm", "boisterous": "sarcasm",
    "clamorous": "sarcasm", "uproarious": "sarcasm", "riotous": "sarcasm", "tumultuous": "sarcasm",
    "turbulent": "sarcasm", "disorderly": "sarcasm", "chaotic": "sarcasm", "anarchic": "sarcasm",
    "lawless": "sarcasm", "uncontrolled": "sarcasm", "wild": "sarcasm", "untamed": "sarcasm",
    "feral": "sarcasm", "savage": "sarcasm", "barbaric": "sarcasm", "primitive": "sarcasm",
    "uncivilized": "sarcasm", "unsophisticated": "sarcasm", "crude": "sarcasm", "rough": "sarcasm",
    "unrefined": "sarcasm", "unpolished": "sarcasm", "unfinished": "sarcasm", "incomplete": "sarcasm",
    "deficient": "sarcasm", "lacking": "sarcasm", "wanting": "sarcasm", "meager": "sarcasm",
    "scanty": "sarcasm", "sparse": "sarcasm", "thin": "sarcasm", "lean": "sarcasm",
    "emaciated": "sarcasm", "gaunt": "sarcasm", "skeletal": "sarcasm", "skinny": "sarcasm",
    "slim": "sarcasm", "slender": "sarcasm", "delicate": "sarcasm", "fragile": "sarcasm",
    "brittle": "sarcasm", "frail": "sarcasm", "weak": "sarcasm", "feeble": "sarcasm",
    "infirm": "sarcasm", "ailing": "sarcasm", "sick": "sarcasm", "unwell": "sarcasm",
    "ill": "sarcasm", "diseased": "sarcasm", "unhealthy": "sarcasm", "toxic": "sarcasm",
    "poisonous": "sarcasm", "venomous": "sarcasm", "noxious": "sarcasm", "harmful": "sarcasm",
    "damaging": "sarcasm", "destructive": "sarcasm", "ruinous": "sarcasm", "deleterious": "sarcasm",
    "detrimental": "sarcasm", "adverse": "sarcasm", "unfavorable": "sarcasm", "negative": "sarcasm",
    "bad": "sarcasm", "evil": "sarcasm", "malignant": "sarcasm", "vicious": "sarcasm",
    "cruel": "sarcasm", "brutal": "sarcasm", "savage": "sarcasm", "ruthless": "sarcasm",
    "merciless": "sarcasm", "heartless": "sarcasm", "cold": "sarcasm", "unfeeling": "sarcasm",
    "insensitive": "sarcasm", "callous": "sarcasm", "unsympathetic": "sarcasm", "uncompassionate": "sarcasm",
    "uncaring": "sarcasm", "indifferent": "sarcasm", "apathetic": "sarcasm", "passive": "sarcasm",
    "unresponsive": "sarcasm", "lifeless": "sarcasm", "inert": "sarcasm", "motionless": "sarcasm",
    "still": "sarcasm", "silent": "sarcasm", "quiet": "sarcasm", "peaceful": "sarcasm",
    "tranquil": "sarcasm", "serene": "sarcasm", "calm": "sarcasm", "placid": "sarcasm",
    "undisturbed": "sarcasm", "unruffled": "sarcasm", "composed": "sarcasm", "collected": "sarcasm",
    "poised": "sarcasm", "dignified": "sarcasm", "stately": "sarcasm", "majestic": "sarcasm",
    "grand": "sarcasm", "impressive": "sarcasm", "awe-inspiring": "sarcasm", "breathtaking": "sarcasm",
    "stunning": "sarcasm", "gorgeous": "sarcasm", "beautiful": "sarcasm", "lovely": "sarcasm",
    "pretty": "sarcasm", "attractive": "sarcasm", "appealing": "sarcasm", "charming": "sarcasm",
    "delightful": "sarcasm", "pleasing": "sarcasm", "enjoyable": "sarcasm", "agreeable": "sarcasm",
    "pleasant": "sarcasm", "nice": "sarcasm", "good": "sarcasm", "excellent": "sarcasm",
    "superb": "sarcasm", "outstanding": "sarcasm", "remarkable": "sarcasm", "notable": "sarcasm",
    "distinguished": "sarcasm", "prominent": "sarcasm", "renowned": "sarcasm", "celebrated": "sarcasm",
    "famous": "sarcasm", "well-known": "sarcasm", "popular": "sarcasm", "favored": "sarcasm",
    "beloved": "sarcasm", "cherished": "sarcasm", "treasured": "sarcasm", "precious": "sarcasm",
    "valuable": "sarcasm", "priceless": "sarcasm", "invaluable": "sarcasm", "irreplaceable": "sarcasm",
    "unique": "sarcasm", "rare": "sarcasm", "uncommon": "sarcasm", "unusual": "sarcasm",
    "peculiar": "sarcasm", "odd": "sarcasm", "strange": "sarcasm", "bizarre": "sarcasm",
    "weird": "sarcasm", "funny": "sarcasm", "amusing": "sarcasm", "hilarious": "sarcasm",
    "comical": "sarcasm", "witty": "sarcasm", "clever": "sarcasm", "intelligent": "sarcasm",
    "smart": "sarcasm", "bright": "sarcasm", "brilliant": "sarcasm", "wise": "sarcasm",
    "knowledgeable": "sarcasm", "learned": "sarcasm", "erudite": "sarcasm", "scholarly": "sarcasm",
    "academic": "sarcasm", "intellectual": "sarcasm", "cerebral": "sarcasm", "thoughtful": "sarcasm",
    "pensive": "sarcasm", "reflective": "sarcasm", "contemplative": "sarcasm", "meditative": "sarcasm",
    "dreamy": "sarcasm", "imaginative": "sarcasm", "creative": "sarcasm", "inventive": "sarcasm",
    "innovative": "sarcasm", "original": "sarcasm", "resourceful": "sarcasm", "ingenious": "sarcasm",
    "clever": "sarcasm", "dexterous": "sarcasm", "skillful": "sarcasm", "adept": "sarcasm",
    "expert": "sarcasm", "proficient": "sarcasm", "masterful": "sarcasm", "virtuoso": "sarcasm",
    "accomplished": "sarcasm", "talented": "sarcasm", "gifted": "sarcasm", "brilliant": "sarcasm",
    "prodigious": "sarcasm", "exceptional": "sarcasm", "extraordinary": "sarcasm", "phenomenal": "sarcasm",
    "remarkable": "sarcasm", "unforgettable": "sarcasm", "memorable": "sarcasm", "impressive": "sarcasm",
    "striking": "sarcasm", "stunning": "sarcasm", "dazzling": "sarcasm", "brilliant": "sarcasm",
    "radiant": "sarcasm", "luminous": "sarcasm", "gleaming": "sarcasm", "shining": "sarcasm",
    "sparkling": "sarcasm", "glittering": "sarcasm", "shimmering": "sarcasm", "glistening": "sarcasm",
    "twinkling": "sarcasm", "flashing": "sarcasm", "blazing": "sarcasm", "fiery": "sarcasm",
    "burning": "sarcasm", "hot": "sarcasm", "sizzling": "sarcasm", "scorching": "sarcasm",
    "searing": "sarcasm", "blistering": "sarcasm", "sweltering": "sarcasm", "torrid": "sarcasm",
    "tropical": "sarcasm", "humid": "sarcasm", "damp": "sarcasm", "moist": "sarcasm",
    "wet": "sarcasm", "soggy": "sarcasm", "drenched": "sarcasm", "soaked": "sarcasm",
    "saturated": "sarcasm", "waterlogged": "sarcasm", "flooded": "sarcasm", "submerged": "sarcasm",
    "underwater": "sarcasm", "aquatic": "sarcasm", "marine": "sarcasm", "oceanic": "sarcasm",
    "sea": "sarcasm", "coastal": "sarcasm", "shoreline": "sarcasm", "beach": "sarcasm",
    "sandy": "sarcasm", "rocky": "sarcasm", "mountainous": "sarcasm", "hilly": "sarcasm",
    "flat": "sarcasm", "level": "sarcasm", "even": "sarcasm", "smooth": "sarcasm",
    "slippery": "sarcasm", "rough": "sarcasm", "bumpy": "sarcasm", "uneven": "sarcasm",
    "jagged": "sarcasm", "sharp": "sarcasm", "pointed": "sarcasm", "blunt": "sarcasm",
    "dull": "sarcasm", "flat": "sarcasm", "boring": "sarcasm", "monotonous": "sarcasm",
    "tedious": "sarcasm", "dreary": "sarcasm", "dull": "sarcasm", "uninteresting": "sarcasm",
    "unexciting": "sarcasm", "uninspiring": "sarcasm", "unimaginative": "sarcasm", "unoriginal": "sarcasm",
    "uncreative": "sarcasm", "uninventive": "sarcasm", "unresourceful": "sarcasm", "ungainly": "sarcasm",
    "clumsy": "sarcasm", "awkward": "sarcasm", "gauche": "sarcasm", "inelegant": "sarcasm",
    "ungraceful": "sarcasm", "uncoordinated": "sarcasm", "unskilled": "sarcasm", "inept": "sarcasm",
    "incompetent": "sarcasm", "incapable": "sarcasm", "unfit": "sarcasm", "unsuitable": "sarcasm",
    "improper": "sarcasm", "inappropriate": "sarcasm", "unseemly": "sarcasm", "indecorous": "sarcasm",
    "rude": "sarcasm", "impolite": "sarcasm", "discourteous": "sarcasm", "unmannerly": "sarcasm",
    "ill-mannered": "sarcasm", "bad-mannered": "sarcasm", "uncivil": "sarcasm", "insolent": "sarcasm",
    "impertinent": "sarcasm", "presumptuous": "sarcasm", "arrogant": "sarcasm", "haughty": "sarcasm",
    "supercilious": "sarcasm", "condescending": "sarcasm", "patronizing": "sarcasm",
    "disdainful": "sarcasm", "scornful": "sarcasm", "contemptuous": "sarcasm", "sarcastic": "sarcasm"
}


def translate_to_genz(text, mapping):
    """
    Translates a given text from standard English to Gen Z slang using a provided mapping.
    It performs a case-insensitive replacement.
    """
    translated_text = text
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)

    for english_word in sorted_keys:
        slang_word = mapping[english_word]
        translated_text = re.sub(r'\b' + re.escape(english_word) + r'\b', slang_word, translated_text, flags=re.IGNORECASE)
    return translated_text

# Initialize the ChatGoogleGenerativeAI model.
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Define the custom prompt for the chatbot.
custom_template = """
You are MoneyMentor, an AI financial literacy coach designed for teenagers.
Your goal is to provide helpful, easy-to-understand financial advice.
Always respond in a friendly, encouraging tone and use Gen Z slang naturally
to make the conversation engaging and relatable.
Make sure to explain financial concepts in a way that makes sense for teens.

Chat History:
{chat_history}

Relevant Information:
{context}

Question: {question}
Answer in Gen Z slang:
"""
CUSTOM_CHAT_PROMPT = PromptTemplate.from_template(custom_template)

# Function to get chatbot response
def get_chatbot_response(user_input, chat_history):
    # Initialize memory for each call, but populate it with past history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    for human_message, ai_message in chat_history:
        memory.save_context({"input": human_message}, {"output": ai_message})

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": CUSTOM_CHAT_PROMPT}
    )
    
    response = qa_chain.invoke({"question": user_input})
    ai_response = response['answer']
    final_response = translate_to_genz(ai_response, GENZ_slang_mapping)
    return final_response