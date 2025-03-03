pub mod llm_tasks;

use clap::{Parser, Subcommand};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum LlmTaskErrors {
    #[error("Argument error: {0}")]
    ArgError(String),
    #[error("Task error: {0}")]
    TaskError(String),
    #[error("Unknown error {0}")]
    Uknown(String),
}

#[derive(Parser, Debug)]
pub struct Args {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug, Clone)]
pub enum Commands {
    Summarize {
        // not required, if not provided, use clipboard
        #[clap(short, long)]
        text: Option<String>,
        #[clap(short, long)]
        clipboard: bool,
    },
}

impl Args {
    pub fn execute(
        &self,
        owui_api_url: &str,
        owui_api_key: &str,
        default_summary_model: &str,
        default_summary_temperature: f64,
    ) -> Result<(), LlmTaskErrors> {
        match &self.command {
            Commands::Summarize { text, clipboard } => {
                let text = if *clipboard {
                    arboard::Clipboard::new()
                        .map_err(|e| LlmTaskErrors::ArgError(e.to_string()))?
                        .get_text()
                        .map_err(|e| LlmTaskErrors::ArgError(e.to_string()))?
                } else if let Some(text_content) = text {
                    text_content.to_owned()
                } else {
                    return Err(LlmTaskErrors::ArgError("No text provided".to_string()));
                };
                let runtime = tokio::runtime::Runtime::new()
                    .map_err(|e| LlmTaskErrors::Uknown(e.to_string()))?;
                runtime.block_on(async {
                    let llmt = llm_tasks::LlmTasks::new(
                        owui_api_key,
                        owui_api_url,
                        default_summary_model,
                        default_summary_temperature,
                    );
                    let res = llmt
                        .summarize(&text)
                        .await
                        .map_err(|e| LlmTaskErrors::Uknown(e.to_string()))?;
                    println!("{}", res);
                    Ok(())
                })
            }
        }
    }
}
