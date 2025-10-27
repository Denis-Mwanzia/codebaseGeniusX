// Navigator Agent - Repository Mapper
// Clones GitHub repository and builds file tree

walker navigator {
    has github_url;
    has repo_path;
    has file_tree = {};
    has readme_summary = "";
    
    can git_clone_repo, build_file_tree, summarize_readme;
    
    nav_node = spawn here node::navigator;
    
    nav_node {
        std.out("🗺️ Navigator: Cloning repository...");
        
        // Clone repository
        repo_path = git_clone_repo(github_url);
        
        if (repo_path != null):
            std.out("🗺️ Navigator: Repository cloned to " + repo_path);
            
            // Build file tree
            file_tree = build_file_tree(repo_path);
            std.out("🗺️ Navigator: File tree built with " + file_tree.children.length + " items");
            
            // Summarize README using Gemini
            readme_summary = summarize_readme(repo_path);
            std.out("🗺️ Navigator: README summarized");
            
            // Move to Inspector
            spawn here walker::inspector(repo_path=repo_path, file_tree=file_tree, readme_summary=readme_summary);
        else:
            std.err("🗺️ Navigator: Failed to clone repository");
    }
}

node navigator (anchor nav_anchor);

