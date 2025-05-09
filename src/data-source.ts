import { DataSource } from "typeorm";
import {
    SideEntity, FactionEntity, TypeEntity, SubtypeEntity,
    SettypeEntity, CycleEntity, SetEntity,
    FormatEntity, PoolEntity, RestrictionEntity, SnapshotEntity,
    CardEntity, PrintingEntity, RulingEntity,
} from "netrunner-entities";

export const AppDataSource = new DataSource({
    database: "result/netrunner.sqlite",
    type: "better-sqlite3",
    logging: ["error", "warn", "info", "log", "migration"],
    entities: [
        SideEntity, FactionEntity, TypeEntity, SubtypeEntity,
        SettypeEntity, CycleEntity, SetEntity,
        FormatEntity, PoolEntity, RestrictionEntity, SnapshotEntity,
        CardEntity, PrintingEntity, RulingEntity
    ],
    migrations: ["./migrations/*.ts"],
    prepareDatabase: db => {
        db.pragma('journal_mode = WAL');
    }
});
