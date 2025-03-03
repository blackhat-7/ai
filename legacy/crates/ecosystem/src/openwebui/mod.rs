pub mod backup;

use anyhow::Result;
use clap::{Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser, Debug)]
pub struct Args {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug, Clone)]
pub enum Commands {
    Backup {
        #[clap(short, long)]
        backup_dir: PathBuf,
    },
}

impl Args {
    pub fn execute(&self) -> Result<()> {
        match &self.command {
            Commands::Backup { backup_dir } => backup::backup(&backup_dir),
        }
    }
}
