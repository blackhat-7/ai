use rig::providers::{gemini, openai};

pub struct React {}

pub trait Reasoner {
    fn reason(&self, input: &str) -> String;
}

pub trait Actor {
    fn act(&self, input: &str) -> String;
}

pub trait Observer {
    fn observe(&self, input: &str) -> String;
}

// llm client
pub struct SimpleReasoner {
    openai_client: openai::Client,
    gemini_client: gemini::Client,
}

// multiple tools
pub struct SimpleActor {
    web_search_tool
}

// filter/process the tool output
pub struct SimpleObserver {}

impl SimpleReasoner {
    pub fn new() -> Self {
        SimpleReasoner {}
    }
}

impl Reasoner for SimpleReasoner {
    fn reason(&self, input: &str) -> String {
        format!("Reasoning about {}", input)
    }
}

impl Actor for SimpleActor {
    fn act(&self, input: &str) -> String {
        format!("Acting on {}", input)
    }
}

impl Observer for SimpleObserver {
    fn observe(&self, input: &str) -> String {
        format!("Observing {}", input)
    }
}
