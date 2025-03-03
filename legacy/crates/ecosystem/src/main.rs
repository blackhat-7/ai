mod deep_research;
mod llm_scraper;
mod openwebui;
mod utils;

use clap::{Parser, Subcommand};
use dotenv::dotenv;

struct EnvVariables {
    crawl4ai_endpoint: String,
}

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[clap(name = "ai", version)]
struct Args {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    Openwebui(openwebui::Args),
    LlmScrape(llm_scraper::Args),
}

fn main() {
    let env_vars = load_env();
    let args = Args::parse();
    match args.command {
        Commands::Openwebui(options) => {
            options.execute().unwrap();
        }
        Commands::LlmScrape(options) => {
            options.execute(env_vars.crawl4ai_endpoint).unwrap();
        }
    }
}

fn load_env() -> EnvVariables {
    dotenv().ok();
    let crawl4ai_endpoint = std::env::var("CRAWL4AI_ENDPOINT").expect("CRAWL4AI_ENDPOINT not set");
    EnvVariables { crawl4ai_endpoint }
}
