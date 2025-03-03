use ai::llm_scraper;
use ai::llm_tasks;
use ai::openwebui;

use clap::{Parser, Subcommand};
use dotenv::dotenv;
use thiserror::Error;

#[derive(Debug, Error)]
enum GeneralError {
    #[error("Failed to load environment variables")]
    EnvLoadError(String),
}

struct EnvVariables {
    crawl4ai_endpoint: String,
    owui_api_url: String,
    owui_api_key: String,
    default_summary_model: String,
    default_summary_temperature: f64,
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
    LlmTasks(llm_tasks::Args),
}

fn main() {
    let env_vars = load_env().unwrap();
    let args = Args::parse();
    match args.command {
        Commands::Openwebui(options) => {
            options.execute().unwrap();
        }
        Commands::LlmScrape(options) => {
            options.execute(&env_vars.crawl4ai_endpoint).unwrap();
        }
        Commands::LlmTasks(options) => {
            options
                .execute(
                    &env_vars.owui_api_url,
                    &env_vars.owui_api_key,
                    &env_vars.default_summary_model,
                    env_vars.default_summary_temperature,
                )
                .unwrap();
        }
    }
}

fn load_env() -> Result<EnvVariables, GeneralError> {
    dotenv().ok();
    let crawl4ai_endpoint = std::env::var("CRAWL4AI_ENDPOINT").expect("CRAWL4AI_ENDPOINT not set");
    let owui_api_url = std::env::var("OWUI_API_URL").expect("OWUI_API_URL");
    let owui_api_key = std::env::var("OWUI_API_KEY").expect("OWUI_API_KEY");
    let default_summary_model =
        std::env::var("DEFAULT_SUMMARY_MODEL").expect("DEFAULT_SUMMARY_MODEL");
    let default_summary_temperature = std::env::var("DEFAULT_SUMMARY_TEMPERATURE")
        .expect("DEFAULT_SUMMARY_TEMPERATURE")
        .parse::<f64>()
        .map_err(|e| GeneralError::EnvLoadError(e.to_string()))?;
    Ok(EnvVariables {
        crawl4ai_endpoint,
        owui_api_url,
        owui_api_key,
        default_summary_model,
        default_summary_temperature,
    })
}
