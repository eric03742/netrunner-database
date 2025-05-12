import { DataSource } from "typeorm";
import {
    SideEntity, FactionEntity, TypeEntity, SubtypeEntity,
    SettypeEntity, CycleEntity, SetEntity,
    FormatEntity, PoolEntity, RestrictionEntity, SnapshotEntity,
    CardEntity, PrintingEntity, RulingEntity,
} from "netrunner-entities";
import path from "path";

const DATABASE_FILENAME = path.join("result", "netrunner.sqlite");

export const AppDataSource = new DataSource({
    database: DATABASE_FILENAME,
    type: "better-sqlite3",
    logging: [
        "error", "warn", "info", "log", "migration",
    ],
    entities: [
        SideEntity, FactionEntity, TypeEntity, SubtypeEntity,
        SettypeEntity, CycleEntity, SetEntity,
        FormatEntity, PoolEntity, RestrictionEntity, SnapshotEntity,
        CardEntity, PrintingEntity, RulingEntity,
    ],
    migrations: [
        "./migrations/*.ts",
    ],
    prepareDatabase: db => {
        db.pragma('journal_mode = WAL');
    }
});
