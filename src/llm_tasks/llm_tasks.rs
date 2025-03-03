use rig::{completion::Prompt, providers::openai};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum LlmTaskErrors {
    #[error("SummaryError: {0}")]
    SummaryError(String),
}

pub struct LlmTasks {
    llm_client: openai::Client,
    default_summary_model: String,
    default_summary_temperature: f64,
}

impl LlmTasks {
    pub fn new(
        owui_api_key: &str,
        owui_api_url: &str,
        default_summary_model: &str,
        default_summary_temperature: f64,
    ) -> Self {
        let llm_client = openai::Client::from_url(owui_api_key, owui_api_url);
        dbg!(owui_api_key, owui_api_url);
        LlmTasks {
            llm_client,
            default_summary_model: default_summary_model.to_string(),
            default_summary_temperature,
        }
    }

    pub async fn summarize(&self, text: &str) -> Result<String, LlmTaskErrors> {
        let agent = self.llm_client.agent(&self.default_summary_model)
            .preamble("You are a summarizer. You summarizer everything perfectly, keeping all the important details and removing unnecessary information.")
            .temperature(self.default_summary_temperature)
            .build();

        Ok(agent
            .prompt(format!("Summarize the following text: {}", text))
            .await
            .map_err(|e| LlmTaskErrors::SummaryError(e.to_string()))?)
    }
}
