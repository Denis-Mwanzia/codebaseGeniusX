// Codebase Genius X - The Intelligent Crew
// Main orchestrator for multi-agent documentation system

walker init {
    root {
        spawn here graph::codebase_genius_workflow;
    }
}

walker captain {
    has github_url;
    has mission_status = {};
    
    root {
        std.out("🧭 Captain: Starting mission for " + github_url);
        
        mission_status = {
            "status": "started",
            "repo_url": github_url,
            "timestamp": std.time_now()
        };
        
        spawn here walker::navigator(github_url=github_url);
    }
}

graph codebase_genius_workflow {
    has anchor workflow_root;
    
    spawn {
        workflow_root = spawn node::workflow;
    }
}

node workflow (anchor workflow_anchor);

