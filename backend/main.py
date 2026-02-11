from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
import random
from PIL import Image
import io
import os
import json
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from ultralytics import YOLO

app = FastAPI()

# --- Security Configuration ---
SECRET_KEY = "soil-ai-secret-key-super-secure"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Database Setup (JSON) ---
DB_PATH = "users.json"
if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump({}, f)

def get_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

# --- Models ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ForgotPassword(BaseModel):
    email: str

# --- Helper Functions ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    db = get_db()
    if username not in db:
        raise credentials_exception
    return db[username]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "soil_model.pt")
try:
    model = YOLO(MODEL_PATH)
    print("AI Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- Auth Endpoints ---

@app.post("/register")
async def register(user: UserCreate):
    db = get_db()
    if user.username in db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    for u in db.values():
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
            
    db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": get_password_hash(user.password),
        "created_at": str(datetime.now())
    }
    save_db(db)
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    user = db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/forgot-password")
async def forgot_password(data: ForgotPassword):
    db = get_db()
    user_found = False
    for u in db.values():
        if u["email"] == data.email:
            user_found = True
            break
    
    if not user_found:
        return {"message": "If the email is registered, you will receive a reset link shortly."}
        
    return {"message": "Password reset link sent (Simulated). Check your email."}

# --- Analysis Endpoint (Protected) ---

@app.post("/analyze")
async def analyze_soil(image: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if model is None:
        raise HTTPException(status_code=500, detail="AI Model not ready.")

    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        results = model.predict(img)
        probs = results[0].probs
        class_idx = probs.top1
        class_name = results[0].names[class_idx]
        conf = float(probs.top1conf)
        
        final_result = generate_mock_analysis(class_name, conf * 100)
        final_result["status"] = "success"
        return final_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

def generate_mock_analysis(soil_type: str, confidence: float):
    data = {
        "Black Soil": {
            "type": "Black (Chernozem)",
            "texture": "Clayey / Heavy",
            "ph": (6.5, 7.8),
            "n": (45, 70), "p": (25, 45), "k": (50, 90), "om": (5, 9),
            "moisture": (15, 25), "water_retention": "High",
            "ec": (0.5, 1.2), "cec": "Low to Moderate",
            "micro": {"Boron": "0.5 ppm", "Iron": "4.5 ppm", "Zinc": "0.8 ppm", "Manganese": "12 ppm"},
            "season": "Post-Monsoon (Rabi)",
            "temp": (20, 30), "drainage": "Slow", "compaction": "Moderate",
            "climate": "Semi-Arid / Temperate",
            "deficiencies": ["Zinc", "Nitrogen", "Boron"],
            "fertilizer": "Urea, Zinc Sulphate, and Borax",
            "crops": ["Cotton", "Wheat", "Linseed", "Tobacco", "Gram"]
        },
        "Cinder Soil": {
            "type": "Cinder (Volcanic)",
            "texture": "Porous / Sandy",
            "ph": (5.8, 6.8),
            "n": (10, 25), "p": (30, 60), "k": (40, 70), "om": (1, 3),
            "moisture": (5, 12), "water_retention": "Very Low",
            "ec": (0.8, 2.0), "cec": "High",
            "micro": {"Boron": "1.2 ppm", "Iron": "25 ppm", "Zinc": "2.5 ppm", "Manganese": "40 ppm"},
            "season": "Year-round with irrigation",
            "temp": (15, 35), "drainage": "Excessive", "compaction": "None",
            "climate": "Volcanic Regions / Tropical",
            "deficiencies": ["Phosphorus", "Potassium", "Nitrogen"],
            "fertilizer": "NPK 10-26-26 and Ammonium Nitrate",
            "crops": ["Coffee", "Grapes", "Potatoes", "Succulents", "Orchids"]
        },
        "Laterite Soil": {
            "type": "Laterite (Red)",
            "texture": "Gravelly / Loamy",
            "ph": (4.5, 6.0),
            "n": (15, 30), "p": (10, 20), "k": (20, 40), "om": (2, 4),
            "moisture": (10, 18), "water_retention": "Low",
            "ec": (0.2, 0.6), "cec": "Very Low",
            "micro": {"Boron": "0.2 ppm", "Iron": "15 ppm", "Zinc": "0.4 ppm", "Manganese": "5 ppm"},
            "season": "Monsoon (Kharif)",
            "temp": (25, 40), "drainage": "Fast", "compaction": "Low",
            "climate": "Tropical Wet / Monsoon",
            "deficiencies": ["Nitrogen", "Lime", "Phosphorus"],
            "fertilizer": "DAP, Lime, and Rock Phosphate",
            "crops": ["Cashew", "Rubber", "Tea", "Coffee", "Coconut"]
        },
        "Peat Soil": {
            "type": "Peat (Muck)",
            "texture": "Spongy / Fibrous",
            "ph": (3.5, 5.2),
            "n": (50, 90), "p": (5, 15), "k": (10, 25), "om": (30, 60),
            "moisture": (40, 70), "water_retention": "Extreme",
            "ec": (0.1, 0.4), "cec": "Extremely High",
            "micro": {"Boron": "0.1 ppm", "Iron": "8 ppm", "Zinc": "0.2 ppm", "Manganese": "2 ppm"},
            "season": "Summer (Zaid)",
            "temp": (10, 25), "drainage": "Poor (Waterlogged)", "compaction": "None (Soft)",
            "climate": "Cold Wet / Marshy",
            "deficiencies": ["Potassium", "Copper", "Molybdenum"],
            "fertilizer": "MOP (Muriate of Potash) and Copper Sulphate",
            "crops": ["Blueberries", "Cranberries", "Sphagnum", "Rice", "Muck-land Vegetables"]
        },
        "Yellow Soil": {
            "type": "Yellow (Podzolic)",
            "texture": "Silty / Clay",
            "ph": (5.0, 6.5),
            "n": (20, 40), "p": (15, 30), "k": (30, 50), "om": (3, 5),
            "moisture": (12, 20), "water_retention": "Moderate",
            "ec": (0.3, 0.8), "cec": "Moderate",
            "micro": {"Boron": "0.4 ppm", "Iron": "5 ppm", "Zinc": "0.6 ppm", "Manganese": "10 ppm"},
            "season": "Spring / Kharif",
            "temp": (18, 30), "drainage": "Moderate", "compaction": "High",
            "climate": "Humid Subtropical",
            "deficiencies": ["Iron", "Magnesium", "Calcium"],
            "fertilizer": "Chelated Iron, Magnesium Nitrate, and Gypsum",
            "crops": ["Paddy", "Citrus", "Soybeans", "Tea", "Cereals"]
        }
    }
    
    stats = data.get(soil_type, data["Yellow Soil"])
    
    return {
        "confidence": f"{confidence:.1f}%",
        "soil_type": stats["type"],
        "texture": stats["texture"],
        "ph_min": stats["ph"][0],
        "ph_max": stats["ph"][1],
        "nitrogen": f"{random.randint(stats['n'][0], stats['n'][1])} mg/kg",
        "phosphorus": f"{random.randint(stats['p'][0], stats['p'][1])} mg/kg",
        "potassium": f"{random.randint(stats['k'][0], stats['k'][1])} mg/kg",
        "organic_matter": f"{random.uniform(stats['om'][0], stats['om'][1]):.1f}%",
        "moisture": f"{random.randint(stats['moisture'][0], stats['moisture'][1])}%",
        "water_retention": stats["water_retention"],
        "salinity_ec": f"{random.uniform(stats['ec'][0], stats['ec'][1]):.2f} dS/m",
        "cec": stats["cec"],
        "micro_nutrients": stats["micro"],
        "planting_season": stats["season"],
        "optimal_temp": f"{stats['temp'][0]}°C - {stats['temp'][1]}°C",
        "drainage_type": stats["drainage"],
        "compaction_level": stats["compaction"],
        "climate_zone": stats["climate"],
        "possible_deficiencies": stats["deficiencies"],
        "recommended_fertilizer": stats["fertilizer"],
        "recommended_crops": stats["crops"],
        "health_score": f"{random.randint(65, 98)}/100"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
