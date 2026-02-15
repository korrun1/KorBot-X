use std::error::Error;
use std::fs::File;
use csv::{ReaderBuilder, WriterBuilder};

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("raw_data.csv")?;
    let mut rdr = ReaderBuilder::new().from_reader(file);
    let mut wtr = WriterBuilder::new().from_path("processed_data.csv")?;

    wtr.write_record(&["time", "high", "low", "close", "atr", "adx"])?;

    let period = 14;
    let mut prev_close = 0.0;
    let mut prev_atr = 0.0;
    let mut prev_plus_dm = 0.0;
    let mut prev_minus_dm = 0.0;
    let mut prev_adx = 0.0;

    for result in rdr.records() {
        let record = result?;
        let time = &record[0];
        let high: f64 = record[1].parse()?;
        let low: f64 = record[2].parse()?;
        let close: f64 = record[3].parse()?;

        // ATR manual calculation
        let tr = f64::max(high - low, f64::max(high - prev_close, low - prev_close).abs());
        let atr_value = ((prev_atr * (period as f64 - 1.0)) + tr) / period as f64;

        // ADX manual calculation (simplified)
        let plus_dm = high - prev_close;
        let minus_dm = prev_close - low;
        let smoothed_plus_dm = ((prev_plus_dm * (period as f64 - 1.0)) + plus_dm) / period as f64;
        let smoothed_minus_dm = ((prev_minus_dm * (period as f64 - 1.0)) + minus_dm) / period as f64;
        let plus_di = 100.0 * smoothed_plus_dm / atr_value;
        let minus_di = 100.0 * smoothed_minus_dm / atr_value;
        let dx = 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di);
        let adx_value = ((prev_adx * (period as f64 - 1.0)) + dx) / period as f64;

        wtr.write_record(&[time, &high.to_string(), &low.to_string(), &close.to_string(), &atr_value.to_string(), &adx_value.to_string()])?;

        prev_close = close;
        prev_atr = atr_value;
        prev_plus_dm = smoothed_plus_dm;
        prev_minus_dm = smoothed_minus_dm;
        prev_adx = adx_value;
    }

    wtr.flush()?;
    println!("Rust processed data successfully!");
    Ok(())
}