use std::error::Error;
use std::fs::File;
use csv::ReaderBuilder;

pub fn process_raw_data(file_path: &str) -> Result<(), Box<dyn Error>> {
    let file = File::open(file_path)?;
    let mut rdr = ReaderBuilder::new().from_reader(file);

    for result in rdr.records() {
        let record = result?;
        println!("{:?}", record);
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_raw_data() {
        // For now, just a placeholder test
        assert_eq!(2 + 2, 4);
    }
}