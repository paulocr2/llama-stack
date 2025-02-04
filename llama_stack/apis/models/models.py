# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Any, Dict, List, Literal, Optional, Protocol, runtime_checkable

from llama_models.schema_utils import json_schema_type, webmethod
from pydantic import BaseModel, ConfigDict, Field

from llama_stack.apis.resource import Resource, ResourceType


class CommonModelFields(BaseModel):
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Any additional metadata for this model",
    )


@json_schema_type
class Model(CommonModelFields, Resource):
    type: Literal[ResourceType.model.value] = ResourceType.model.value

    @property
    def model_id(self) -> str:
        return self.identifier

    @property
    def provider_model_id(self) -> str:
        return self.provider_resource_id

    model_config = ConfigDict(protected_namespaces=())


class ModelInput(CommonModelFields):
    model_id: str
    provider_id: Optional[str] = None
    provider_model_id: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())


@runtime_checkable
class Models(Protocol):
    @webmethod(route="/models/list", method="GET")
    async def list_models(self) -> List[Model]: ...

    @webmethod(route="/models/get", method="GET")
    async def get_model(self, identifier: str) -> Optional[Model]: ...

    @webmethod(route="/models/register", method="POST")
    async def register_model(
        self,
        model_id: str,
        provider_model_id: Optional[str] = None,
        provider_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Model: ...

    @webmethod(route="/models/unregister", method="POST")
    async def unregister_model(self, model_id: str) -> None: ...
