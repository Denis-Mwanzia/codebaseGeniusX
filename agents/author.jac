// Author Agent - Documentation Writer
// Generates structured Markdown documentation using Gemini

walker author {
    has code_graph;
    has file_tree;
    has readme_summary;
    has documentation = "";
    
    can generate_markdown_docs;
    
    auth_node = spawn here node::author;
    
    auth_node {
        std.out("✍️ Author: Writing documentation...");
        
        // Prepare context for documentation generation
        context = {
            "code_graph": code_graph,
            "file_tree": file_tree,
            "readme_summary": readme_summary
        };
        
        // Generate documentation using Gemini
        documentation = generate_markdown_docs(context);
        
        if (documentation != ""):
            std.out("✍️ Author: Documentation generated");
            
            // Move to Designer
            spawn here walker::designer(documentation=documentation, code_graph=code_graph);
        else:
            std.err("✍️ Author: Failed to generate documentation");
    }
}

node author (anchor auth_anchor);

