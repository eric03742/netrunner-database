import connection from "./config.json" with { type: "json" };
import { DataSource } from "typeorm";
import {
    SideEntity, FactionEntity, TypeEntity, SubtypeEntity,
    SettypeEntity, CycleEntity, SetEntity,
    FormatEntity, PoolEntity, RestrictionEntity, SnapshotEntity,
    CardEntity, PrintingEntity, RulingEntity,
} from "@eric03742/netrunner-entities";

export const AppDataSource = new DataSource({
    ...connection,
    type: "mysql",
    logging: ["error", "warn", "info", "log", "migration"],
    entities: [
        SideEntity, FactionEntity, TypeEntity, SubtypeEntity,
        SettypeEntity, CycleEntity, SetEntity,
        FormatEntity, PoolEntity, RestrictionEntity, SnapshotEntity,
        CardEntity, PrintingEntity, RulingEntity
    ],
    migrations: ["./migrations/*.ts"],
});
