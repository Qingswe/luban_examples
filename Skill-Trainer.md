# 训练 Luban Skill

Create a training plan for editing Luban configuration tables, with the goal of generating and iterating on AI skills. Follow these steps:

**1. Training Data Preparation:**
- Use all content from `@datable_docs/zh/manual` as the training corpus for the Skill
- Specifically ensure coverage of:
  - `@datable_docs/zh/manual/excel格式（初级）.md` (Basic Excel format)
  - `@datable_docs/zh/manual/excel格式（高级）.md` (Advanced Excel format)

**2. Training Execution via Subagent:**
- Use subagent to invoke specialized training agents for Luban skill generation
- First phase: Let subagent understand the task requirements and Luban table editing concepts
- Second phase: After task comprehension, use `skill-creator` to output the trained Skill
- Train multiple Skill replicas in parallel (specify number: e.g., 3-5 replicas)
- Store each replica's training results in separate folders with clear naming (e.g., `skill_replica_1/`, `skill_replica_2/`, etc.)
- Configure subagent using `.claude/agents/luban-skill-trainer.md` for training execution

**3. Task Design (Test Case):**
- Design a moderately complex RPG game configuration scenario that exercises ALL features from both:
  - Basic Excel format features (初级)
  - Advanced Excel format features (高级)
- The task should include realistic game design elements such as:
  - Character stats and progression tables
  - Item/equipment configurations
  - Skill trees or ability systems
  - Quest/mission data
  - Localization strings
  - Complex data relationships and references between tables

**4. Evaluation and Iteration:**
- Once skills are generated, invoke each trained skill with the RPG test case
- Evaluate outputs based on criteria such as:
  - Correctness of Luban table syntax
  - Proper use of basic and advanced Excel format features
  - Data integrity and referential consistency
  - Completeness of the RPG configuration
- Assign scores to each skill replica's output
- Iterate the training process based on evaluation results:
  - Identify weaknesses in skill performance
  - Adjust training data or prompts
  - Retrain and re-evaluate until satisfactory results are achieved

**5. Deliverables:**
- Organized folder structure with all skill replicas
- Evaluation scores and comparison matrix
- Final recommended skill version
- Documentation of iteration improvements

Please confirm the number of skill replicas to train and any specific RPG game mechanics you want to prioritize in the test case.