CREATE TABLE IF NOT EXISTS raw_weather_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    temperature DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    cloudcover DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS processed_weather_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    temperature_celsius DOUBLE PRECISION,
    is_raining BOOLEAN,
    is_cloudy BOOLEAN
);
