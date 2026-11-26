You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Test regression with Pydantic 2.14

```
$ git clone https://github.com/BrianPugh/cyclopts.git
$ cd cyclopts
$ uv pip install -e .[trio,yaml,docs,dev]
$ pytest -v
[…]
========================================================================================= FAILURES =========================================================================================
__________________________________________________________________________ test_pydantic_validate_by_alias_false ___________________________________________________________________________

app = App(alias=(), synonym=(), default_command=<function test_pydantic_validate_by_alias_false.<locals>.main at 0x7f132708a...('--version',), help_flags=('--help', '-h'), group=(), validator=[], sort_key=<UNSET>, result_action=('return_value',))
assert_parse_args = <function assert_parse_args.<locals>.inner at 0x7f132708b110>

    def test_pydantic_validate_by_alias_false(app, assert_parse_args):
        """When ``validate_by_alias=False``, the alias is not registered as a CLI option.

        https://github.com/BrianPugh/cyclopts/issues/908

        ``validate_by_alias=False`` tells pydantic to reject the alias during validation
        (it implies ``validate_by_name=True``), so only the field-name CLI option should
        be registered; the alias form must not silently parse into a value the model then
        rejects.
        """

        class Model(BaseModel):
            model_config = ConfigDict(validate_by_alias=False)

            full_name: str = Field(alias="userName")

        @app.default
        def main(model: Model):
            pass

        # The field name is accepted.
>       assert_parse_args(main, "--model.full_name Alice", model=Model.model_validate({"full_name": "Alice"}))

/home/ben/src/forks/cyclopts/tests/test_pydantic.py:313:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/home/ben/src/forks/cyclopts/tests/conftest.py:139: in inner
    actual_command, actual_bind, _ = app.parse_args(cmd, print_error=False, exit_on_error=False)
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/home/ben/src/forks/cyclopts/cyclopts/core.py:2096: in parse_args
    self._handle_parse_error(e, tokens)
/home/ben/src/forks/cyclopts/cyclopts/core.py:2091: in parse_args
    command, bound, _, ignored, _ = self._parse_known_args(
/home/ben/src/forks/cyclopts/cyclopts/core.py:1943: in _parse_known_args
    bound, unused_tokens = create_bound_arguments(
/home/ben/src/forks/cyclopts/cyclopts/bind.py:1277: in create_bound_arguments
    unused_tokens = _parse_pos(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

argument_collection = [Argument(tokens=[], field_info=FieldInfo(names=('model',), kind=<_ParameterKind.POSITIONAL_OR_KEYWORD: 1>, required=T...None, env_var=(), required=True, accepts_keys=None), hint=<class 'str'>, index=0, keys=('full_name',), _value=<UNSET>)]
tokens = ['--model.full_name', 'Alice'], end_of_options_delimiter = '--', contiguous_positional_count = None, preserve_delimiter = False

    def _parse_pos(
        argument_collection: ArgumentCollection,
        tokens: list[str],
        *,
        end_of_options_delimiter: str = "--",
        contiguous_positional_count: int | None = None,
        preserve_delimiter: bool = False,
    ) -> list[str]:
        """Assign positional tokens to positional parameters.

        Parameters
        ----------
        argument_collection: ArgumentCollection
            Arguments whose keyword/flag tokens have already been consumed.
        tokens: list[str]
            Unused tokens from ``_parse_kw_and_flags``.
        end_of_options_delimiter: str
            Delimiter after which all tokens are forced positional. Consumed as a
            marker (standard CLI behavior), unless ``preserve_delimiter``.
        preserve_delimiter: bool
            Keep the delimiter token itself in the captured values (force-positional)
            when the collection has a raw-stream capture parameter. Set when the
            bound tokens are forwarded to another parse — a meta app's
            ``app(tokens)`` — which needs the delimiter to keep the trailing tokens
            protected. Leaf commands keep the standard consume-as-marker behavior.
        contiguous_positional_count: int | None
            If not ``None``, the number of leading contiguous positional tokens
            that were adjacent in the original CLI input (before keyword extraction
            created a gap). Used to cap how many tokens a ``POSITIONAL_ONLY``
            list/iterable parameter may consume, preventing it from greedily
            swallowing tokens that originally appeared after keyword arguments.
            See ``_parse_kw_and_flags`` for how this value is computed.
        """
        prior_positional_or_keyword_supplied_as_keyword_arguments = []

        if not tokens:
            return []

        tokens_and_force_positional = _preprocess_positional_tokens(
            tokens,
            end_of_options_delimiter,
            preserve_delimiter=preserve_delimiter and _captures_raw_stream(argument_collection),
        )

        for i in itertools.count():
            try:
                argument, _, _ = argument_collection.match(i)
            except ValueError:
                break
            if argument.field_info.kind is POSITIONAL_OR_KEYWORD:
                if argument.tokens and argument.tokens[0].keyword is not None:
                    prior_positional_or_keyword_supplied_as_keyword_arguments.append(argument)
                    # Continue in case we hit a VAR_POSITIONAL argument.
                    continue
                if prior_positional_or_keyword_supplied_as_keyword_arguments:
                    if not tokens_and_force_positional:
                        # ``tokens`` contained only the ``--`` end-of-options delimiter;
                        # there are no positional tokens to misassign.
                        break
                    # Use the preprocessed token: ``tokens`` still contains the ``--``
                    # end-of-options delimiter, and ``force_positional`` marks tokens
                    # after it, which must not be treated as options.
                    token, force_positional = tokens_and_force_positional[0]
                    if not force_positional and not argument.parameter.allow_leading_hyphen and is_option_like(token):
                        # It's more meaningful to interpret the token as an intended option,
                        # rather than an intended positional value for ``argument``.
                        raise UnknownOptionError(token=CliToken(value=token), argument_collection=argument_collection)
                    else:
                        raise ArgumentOrderError(
                            argument=argument,
                            prior_positional_or_keyword_supplied_as_keyword_arguments=prior_positional_or_keyword_supplied_as_keyword_arguments,
                            token=token,
                        )

            # Create Token objects for token_count() to enable union type probing.
            # Token creation is cheap (small frozen dataclass). For positional args,
            # we create separate tokens for actual use with per-element indices.
            upcoming_tokens = [CliToken(value=t[0], index=j) for j, t in enumerate(tokens_and_force_positional)]
            tokens_per_element, consume_all = argument.token_count(upcoming_tokens=upcoming_tokens)
            tokens_per_element = max(1, tokens_per_element)

            if consume_all and argument.field_info.kind is POSITIONAL_ONLY:
                # POSITIONAL_ONLY parameters can come after a POSITIONAL_ONLY list/iterable.
                # This makes it easier to create programs that do something like:
                #    $ python my-program.py input_folder/*.csv output.csv

                # Need to see how many tokens we need to leave for subsequent POSITIONAL_ONLY parameters.
                n_tokens_to_leave = _future_positional_only_token_count(argument_collection, i + 1)

                # Cap at the contiguous positional count to prevent consuming tokens
                # that appeared after keyword arguments (issue #763).
                if contiguous_positional_count is not None:
                    n_tokens_to_leave = max(
                        n_tokens_to_leave, len(tokens_and_force_positional) - contiguous_positional_count
                    )
            else:
                n_tokens_to_leave = 0

            new_tokens = []
            while (len(tokens_and_force_positional) - n_tokens_to_leave) > 0:
                if (len(tokens_and_force_positional) - n_tokens_to_leave) < tokens_per_element:
                    raise MissingArgumentError(
                        argument=argument,
                        tokens_so_far=[x[0] for x in tokens_and_force_positional],
                    )

                for index, (token_str, force_positional) in enumerate(tokens_and_force_positional[:tokens_per_element]):
                    if not force_positional and not argument.parameter.allow_leading_hyphen and is_option_like(token_str):
>                       raise UnknownOptionError(token=CliToken(value=token_str), argument_collection=argument_collection)
E                       cyclopts.exceptions.UnknownOptionError: Unknown option: --model.full_name.

/home/ben/src/forks/cyclopts/cyclopts/bind.py:1155: UnknownOptionError
--------------------------------------------------------------------------------- snapshot report summary ----------------------------------------------------------------------------------
24 snapshots passed.
================================================================================= short test summary info ==================================================================================
FAILED tests/test_pydantic.py::test_pydantic_validate_by_alias_false - cyclopts.exceptions.UnknownOptionError: Unknown option: --model.full_name.
=============================================================== 1 failed, 3836 passed, 233 skipped, 13 deselected in 20.71s ================================================================
```

However:

```
$ uv pip install 'pydantic<2.14'
$ pytest -v
[…]
==================================================================== 3837 passed, 233 skipped, 13 deselected in 20.16s =====================================================================
```

This seems to be related to:

- https://github.com/pydantic/pydantic/issues/13716
- https://github.com/pydantic/pydantic/pull/13717
- https://github.com/BrianPugh/cyclopts/issues/908

… but I don’t think I understand the full picture well enough to know what needs to be changed here.
