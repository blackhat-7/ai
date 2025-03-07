pub mod web_tools;

use anyhow::Result;
use clap::{Parser, Subcommand};

#[derive(Parser, Debug)]
pub struct Args {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug, Clone)]
pub enum Commands {
    Scrape {
        #[clap(short, long)]
        url: String,
    },
}

impl Args {
    pub fn execute(&self, crawl4ai_endpoint: &str) -> Result<()> {
        match &self.command {
            Commands::Scrape { url } => {
                let runtime = tokio::runtime::Runtime::new()?;
                runtime.block_on(async {
                    let llm_scraper = web_tools::WebTools::new(crawl4ai_endpoint.to_string());
                    llm_scraper.scrape(&url).await?;
                    Ok(())
                })
            }
        }
    }
}
