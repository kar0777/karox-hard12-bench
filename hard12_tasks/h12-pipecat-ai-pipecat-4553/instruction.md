You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`InterruptionFrame` not serializable via protobuf — interruption may not propagate through pipeline

### pipecat version

1.2.0

### Python version

3.12.0

### Operating System

Ubuntu 26.04

### Issue description

**Environment**
Transport: WebSocketTransport
STT: Deepgram Flux
LLM: Gemini/OpenAI/Claude
TTS: ElevenLabs/Deepgram
Pipecat Flows: Yes

### Reproduction steps

When a user starts speaking, and `LLMUserAggregator` or `DeepgramFluxSTTService` broadcasts an `InterruptionFrame`, the following warning appears twice in the logs:
```
WARNING | pipecat.serializers.protobuf:serialize:96 - Frame type
<class 'pipecat.frames.frames.InterruptionFrame'> is not serializable
```
---
**Questions**

- Is `InterruptionFrame` expected to be unserializable in protobuf? Is this by design?
- Could this cause the `InterruptionFrame` to be silently dropped at a transport hop, preventing it from reaching LLM/TTS services downstream?
- The `InterruptionTaskFrame` arrives at the pipeline task (14:22:04.057) after the node transition already started (14:22:04.052). Is there a guaranteed way to ensure the interruption completes before `FlowManager.set_node_from_config() executes`, from outside a `FrameProcessor`? If not, how to guarantee the interruption will happen based on a timer trigger?

**Additional Context**

This was observed in a timer-driven node transition scenario (Pipecat Flows), where a timer fires, triggering a transition from one node to another regardless of the current conversation state.

**Node transition logic**
```py
async def _transition_node(self, mode: str):
        """
        Transition FlowManager to node for given mode.

        Station-specific node mapping:
        - role_play -> create_role_play_node
        - examiner -> create_examiner_node
        - feedback -> create_feedback_node
        """
        try:
            # business logic

            # Create and transition to new node
            next_node = (
                node_creator(scenario_data, self.flow_manager)
                if is_feedback_mode
                else node_creator(scenario_data)
            )
             # The interruption frame flow
            await self.flow_manager.task.queue_frame(InterruptionTaskFrame(), FrameDirection.UPSTREAM)
            await self.flow_manager.set_node_from_config(next_node)
            logger.info(
                f"[history-taking] FlowManager transitioned to {mode} node for user {self.user_id}"
            )
```

### Expected behavior

The expected behaviour is to interrupt whatever is happening in the pipeline, clear the state, and start the new node afresh. To be precise:
- Interrupt the bot's response
- Interrupt  LLM inference
- Ignore the user's response

### Actual behavior

I have two nodes: role-play and examiner. The bot responded to a question in the role-play node in the examiner node despite the time-driven node transition.

### Logs

```shell
Relevant logs

2026-05-21 14:21:55.252 | DEBUG    | pipecat.services.deepgram.tts:run_tts:351 - DeepgramTTSService#1: Generating TTS [It’s been going on for about four months. ]
2026-05-21 14:21:55.566 | DEBUG    | pipecat.transports.base_output:_bot_started_speaking:655 - Bot started speaking
INFO:     127.0.0.1:33832 - "GET /health HTTP/1.1" 200 OK
2026-05-21 14:21:57.092 | DEBUG    | pipecat.services.tts_service:push_frame:800 - DeepgramTTSService#1 cleaning up TTS context ef24e849-0e35-49f8-b706-b88f4c7a507e
2026-05-21 14:21:58.604 | DEBUG    | pipecat.transports.base_output:_handle_frame:749 - Bot stopped speaking based on TTSStoppedFrame
2026-05-21 14:21:58.604 | DEBUG    | pipecat.transports.base_output:_bot_stopped_speaking:683 - Bot stopped speaking
2026-05-21 14:22:01.915 | DEBUG    | pipecat.processors.aggregators.llm_response_universal:_on_user_turn_started:885 - LLMUserAggregator#1: User started speaking (strategy: VADUserTurnStartStrategy#1)
2026-05-21 14:22:01.916 | DEBUG    | pipecat.processors.frame_processor:broadcast_interruption:706 - LLMUserAggregator#1: broadcasting interruption
2026-05-21 14:22:01.938 | WARNING  | pipecat.serializers.protobuf:serialize:96 - Frame type <class 'pipecat.frames.frames.InterruptionFrame'> is not serializable
2026-05-21 14:22:02.267 | DEBUG    | pipecat.services.deepgram.flux.base:_handle_start_of_turn:590 - User started speaking
2026-05-21 14:22:02.267 | DEBUG    | pipecat.processors.frame_processor:broadcast_interruption:706 - DeepgramFluxSTTService#1: broadcasting interruption
2026-05-21 14:22:02.287 | WARNING  | pipecat.serializers.protobuf:serialize:96 - Frame type <class 'pipecat.frames.frames.InterruptionFrame'> is not serializable
2026-05-21 14:22:04.052 | DEBUG    | pipecat_flows.manager:_set_node:583 - Setting node: examiner
2026-05-21 14:22:04.052 | DEBUG    | pipecat_flows.actions:execute_actions:201 - Successfully executed action: function
2026-05-21 14:22:04.057 | DEBUG    | pipecat.pipeline.task:_source_push_frame:866 - PipelineTask#1: received interruption task frame upstream InterruptionTaskFrame#1
2026-05-21 14:22:04.067 | DEBUG    | pipecat_flows.actions:execute_actions:201 - Successfully executed action: tts_say
2026-05-21 14:22:04.068 | DEBUG    | pipecat_flows.actions:execute_actions:201 - Successfully executed action: function
2026-05-21 14:22:04.083 | INFO     | pipecat.services.ai_service:_update_settings:132 - DeepgramTTSService#1: updated settings fields: {'voice'}
2026-05-21 14:22:04.085 | DEBUG    | pipecat.services.deepgram.tts:_disconnect_websocket:257 - Disconnecting from Deepgram WebSocket
2026-05-21 14:22:04.088 | WARNING  | pipecat.serializers.protobuf:serialize:96 - Frame type <class 'pipecat.frames.frames.InterruptionFrame'> is not serializable
```
