use anyhow::Result;
use std::{path::PathBuf, process::Command};

pub fn which(cmd: &str) -> Result<PathBuf> {
    let output = Command::new("which").arg(cmd).output()?;
    Ok(PathBuf::from(String::from_utf8(output.stdout)?.trim()))
}
