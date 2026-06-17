CREATE TABLE IF NOT EXISTS body_composition_logs (
  date_key TEXT PRIMARY KEY,
  weight REAL,
  body_fat REAL,
  body_fat_mass REAL,
  subcutaneous_fat REAL,
  skeletal_muscle_rate REAL,
  skeletal_muscle_mass REAL,
  bmi REAL,
  visceral_fat REAL,
  basal_metabolism REAL,
  body_age REAL,
  raw_text TEXT,
  source TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS app_settings (
  setting_key TEXT PRIMARY KEY,
  setting_value TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS food_logs (
  date_key TEXT PRIMARY KEY,
  breakfast TEXT,
  lunch TEXT,
  dinner TEXT,
  snack TEXT,
  calories REAL,
  protein REAL,
  fat REAL,
  carbs REAL,
  sugar REAL,
  fiber REAL,
  salt REAL,
  updated_at TEXT NOT NULL
);
